import pandas as pd
import numpy as np


def dropTest(path_bugs, path_metrics):
    df=pd.read_csv(path_bugs)
    df=df[~df.Classe.str.contains("Test", case=False)]
    df.to_csv(path_bugs, index=False)

    colnames=["Commit","Classe","LOC","WMC","RFC","LCOM","CBO","DIT","NOC","impInh","intInh","delegations"]
    inhdf=pd.read_csv(path_metrics, names=colnames)
    inhdf=inhdf[~inhdf.Classe.str.contains("Test", case=False)]
    inhdf.to_csv(path_metrics, index=False)

def merge(path_bugs, path_metrics, path_salvataggio):
    bugsdf=pd.read_csv(path_bugs)
    #USA SOLO SE NON DROPPI TEST PRIMA
    #colnames=["Commit","Classe","LOC","WMC","RFC","LCOM","CBO","DIT","NOC","impInh","intInh","delegations"]
    #inhdf=pd.read_csv(path_metrics, names=colnames)
    inhdf=pd.read_csv(path_metrics)

    #Rimozione estensione .java dal file bugsdf
    bugsdf['Classe']=bugsdf['Classe'].apply(lambda x: x[:-5])

    #merge
    merged=pd.merge(bugsdf,inhdf, how='left', on=['Classe','Commit'])

    merged['BugDaFileEsterno']=0
    merged['Linee aggiunte ESTERNI']=0
    merged['Linee rimosse ESTERNI']=0
    merged['Linee rimosse da file eliminati']=0

    #Segmento per flaggare come buggati i commit che hanno un bug proveniente da uno o più file non .java
    #Si utilizza la colonna BugDaFileEsterno che sarà uguale a 1 per tutte le righe di quel commit.
    #Usare la media in seguito qunado si va a raggruppare per ridurre i dati al singolo commit.

    bug_esterni=merged.loc[((merged['Bug']>=1) & (merged['Classe']=='altr'))]
    commit_da_flaggare=bug_esterni['Commit'].tolist()

    for commit in commit_da_flaggare:
        #print(commit)
        merged.loc[merged['Commit']==commit, 'BugDaFileEsterno']=1

    #Segmento per salvare le aggiunte/rimozioni effettuate sui file esterni.
    #Si utilizza la colonna 'Linee aggiunte ESTERNI' che sarà uguale alle line aggiunte da file esterni per tutte le righe di quel commit.
    #Usare la media in seguito qunado si va a raggruppare per ridurre i dati al singolo commit.

    #Estraggo la lista dei commit che ha dei file esterni modificati
    commit_mod_est=merged.loc[(merged['Classe']=="altr") & ((merged['Linee rimosse']>0) | (merged['Linee aggiunte']>0))]['Commit'].tolist()

    for commit in commit_mod_est:
        #Localizzo le linee aggiunte/rimosse da file esterni per quel commit
        aggiunte=merged.loc[(merged['Commit']==commit) & (merged['Classe']=="altr")]
        aggiunte=aggiunte['Linee aggiunte'].iloc[0]

        rimosse=merged.loc[(merged['Commit']==commit) & (merged['Classe']=="altr")]
        rimosse=rimosse['Linee rimosse'].iloc[0]

        #Per quel commit, inserisco per ogni classe che sono state modificate n linee da file esterni
        merged.loc[merged['Commit']==commit, ['Linee aggiunte ESTERNI', 'Linee rimosse ESTERNI']]=[aggiunte,rimosse]


    #Serve per salvare il numero delle linee rimosse quando un file viene eliminato
    #Essendo che è stato eliminato, non si troverà nella directory del checkout del commit quando si usa swanalytic
    #Quindi col merge verrebbe droppata la linea in seguito. Così viene eliminata lo stesso ma salvo il numero di righe rimosse
    commit_con_file_eliminati=merged.loc[((merged["LCOM"]).isnull()) & (merged["Eliminato"]==1), "Commit"].tolist()
    commit_con_file_eliminati=list(set(commit_con_file_eliminati))
    for commit in commit_con_file_eliminati:

        linee_rimosse_file_el=merged.loc[((merged["Commit"]==commit)&(merged["Eliminato"]==1)&(merged["LCOM"]).isnull()), "Linee rimosse"].tolist()
        tot_linee_rimosse_file_el=sum(linee_rimosse_file_el)
        merged.loc[merged["Commit"]==commit, "Linee rimosse da file eliminati"]=tot_linee_rimosse_file_el



    #AGGIUNTA NUMERO DI FILE MODIFICATI PRIMA DI DROP
    #QUESTO PERCHE' SE QUALCHE FILE VIENE ELIMINATO, IL CSV DI SWANALYTIC NON LO CONTERRA'
    #QUINDI PRIMA DI DROPPARE, DEVO CONTARE QUANTI FILE SONO STATI modificati
    raggruppati=merged.groupby('Commit', sort=False, as_index=False).agg({
                         'Modificata':[('sumModificati','sum')]})
    raggruppati.columns = raggruppati.columns.droplevel()

    raggruppati.rename(columns={list(raggruppati)[0]:'Commit'}, inplace=True)
    print(raggruppati)
    dict=raggruppati.set_index('Commit').T.to_dict("list")
    for commit in dict:
        #sottraggo 1 se vengono modificati file esterni
        if merged.loc[((merged['Commit']==commit)&(merged['Classe']=='altr')),'Modificata'].index[0]==1:
            dict[commit][0]-=1

        merged.loc[(merged['Commit']==commit),'File java modificati']=dict[commit][0]

    print(dict)
    merged=merged.dropna(subset=['LCOM'])
    print(merged)
    merged.to_csv(path_salvataggio,index=False)





#Funzione che crea, a partire dal file contenente commit-CLASSE-bug-modifiche alle linee-metriche di ereditarietà, -continua sotto-
#il file che contiene la media/somma di questi valori rapportato al singolo commit (NON PIU' PER COMMIT-CLASSE)
def createSingleCommitCsv(merge_path, path_salvataggio):
    df=pd.read_csv(merge_path)
    #gruppo=df.groupby(["Commit"], sort=False, as_index=False).sum()[['Commit','Linee aggiunte','Linee rimosse']]
    df['impInh']=df["impInh"].astype(int)
    df['intInh']=df["intInh"].astype(int)
    df['Numero file'] = 1
    #print(df['Numero file'])


    test_gruppi=df.groupby('Commit', sort=False, as_index=False)
    test_gruppi.sum().reset_index().to_csv("/home/gerardo/Scrivania/MergeBugAndInh/ProvaGruppi.csv")
    print("SALVATO")

    gruppo=df.groupby('Commit', sort=False, as_index=False).agg({
                         'Numero file':[('Numero file','sum')],
                         'Linee aggiunte':[('Linee aggiunte','sum')],
                         'Linee rimosse':[('Linee rimosse','sum')],
                         'Linee aggiunte ESTERNI':[('Linee aggiunte ESTERNI','mean')],
                         'Linee rimosse ESTERNI':[('Linee rimosse ESTERNI','mean')],
                         'impInh':[('impInh','sum')],
                         'intInh':[('intInh','sum')],
                         'delegations':[('delegations','sum')],
                         'Bug':[('Bug','max')],
                         'Fix':[('Fix','max')],
                         'LOC':[('mediaLOC','mean'),('sumLOC', 'sum'),('medianLOC', 'median')],
                         'WMC':[('mediaWMC','mean'),('sumWMC', 'sum'),('medianWMC', 'median')],
                         'RFC':[('mediaRFC','mean'),('sumRFC', 'sum'),('medianRFC', 'median')],
                         'LCOM':[('mediaLCOM','mean'),('sumLCOM', 'sum'),('medianLCOM', 'median')],
                         'CBO':[('mediaCBO','mean'),('sumCBO', 'sum'),('medianCBO', 'median')],
                         'DIT':[('mediaDIT','mean'),('sumDIT', 'sum'),('medianDIT', 'median')],
                         'NOC':[('mediaNOC','mean'),('sumNOC', 'sum'),('medianNOC', 'median')],
                         'BugDaFileEsterno':[('BugDaFileEsterno', 'mean')],
                         'Linee rimosse da file eliminati':[('Linee rimosse da file eliminati','mean')],
                         'File java modificati':[('File java modificati', 'mean')]
                         })
    gruppo.columns = gruppo.columns.droplevel()
    gruppo.rename(columns={list(gruppo)[0]:'Commit'}, inplace=True)
    gruppo.to_csv("/home/gerardo/Scrivania/MergeBugAndInh/ProvaGruppi.csv", index=False)
    #Unione dei dati provenienti da file non .java a quelli .java
    for idx in gruppo.index:
        if(gruppo.at[idx,'BugDaFileEsterno']>0 and gruppo.at[idx,'Bug']==0):
            gruppo.at[idx, 'Bug']=gruppo.at[idx,'BugDaFileEsterno']
        gruppo.at[idx,'Linee aggiunte']+=gruppo.at[idx, 'Linee aggiunte ESTERNI']
        gruppo.at[idx,'Linee rimosse']+=gruppo.at[idx, 'Linee rimosse ESTERNI']
        gruppo.at[idx,'Linee rimosse']+=gruppo.at[idx, 'Linee rimosse da file eliminati']



    print(gruppo)
    #Stable, increase, decrease per i bug e i fix (per rendere problema di classificazione)

    listabug=gruppo['Bug'].tolist()
    listafix=gruppo['Fix'].tolist()

    gruppo['Bug'] = gruppo['Bug'].astype(str)
    i=0
    changelist = [0] * len(listabug)
    while i<len(listabug)-1:
        changelist[i]=changelist[i-1]+listabug[i]-listafix[i]
        print(str(changelist[i])+"\t"+str(listabug[i])+"\t"+str(listafix[i]))
        if(changelist[i]==changelist[i-1]):
            gruppo.at[i, 'Bug']='Stable'
            #gruppo.at[i, 'Fix']='Stable'
        else:
            if(changelist[i]>changelist[i-1]):
                gruppo.at[i,'Bug']='Increase'
            else:
                gruppo.at[i,'Bug']='Decrease'
        i+=1
    #gruppo.at[0, 'Bug']='Stable'



    gruppo.to_csv(path_salvataggio, index=False)


path_bugs='/home/gerardo/Scrivania/ver-comm-class/COLLECTIONS_commitFileAggiornati.csv'
path_metrics='/home/gerardo/Scrivania/metricheSwAnalytics/NEWCollectionsMetricsMAIN.csv'
path_salvataggio_merge='/home/gerardo/Scrivania/MergeBugAndInh/ultimoCOLLECTIONS_DROPPEDmergedLEFT2.csv'
path_salvataggio_pronto="/home/gerardo/Scrivania/ReadyDatasets/ultimoDatasetCollectionsTest.csv"
dropTest(path_bugs, path_metrics)
merge(path_bugs,path_metrics,path_salvataggio_merge)
createSingleCommitCsv(path_salvataggio_merge, path_salvataggio_pronto)
