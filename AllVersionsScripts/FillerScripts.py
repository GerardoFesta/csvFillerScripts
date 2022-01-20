import csv
import pandas as pd
import os
import subprocess
import numpy as np
from datetime import datetime, timezone

def cloneProject(finalcsvpath,shpath,repopath,project_url,project_id):
    subprocess.call(['bash',shpath+'clone.sh',project_url,repopath])

def getD4jInfo(finalcsvpath,shpath,repopath,project_url,project_id):
    process=subprocess.Popen(['bash',shpath+'d4jQuery.sh',finalcsvpath,project_id])
    process.wait()
    colnames=['bug.id','revision.id.buggy','revision.id.fixed','report.id','report.url','revision.date.buggy','revision.date.fixed']
    finaldf=pd.read_csv(finalcsvpath, names=colnames)

    finaldf.to_csv(finalcsvpath, index=False)

def getCommitsVersionsDate(finalcsvpath,shpath,repopath,project_url,project_id):
    #esecuzione dello script che genera il csv contenente hash, data e versione
    process=subprocess.Popen(['bash',shpath+'hashDateTag.sh',repopath])
    process.wait()
    #Sezione che estende il tag relativo alla versione x a tutti i tag che si trovano tra il commit con il tag x e quello con il tag x+1
    colnames=['commit', 'data', 'versione','ex1','ex2','ex3']
    df = pd.read_csv(repopath+'/commitsInfo.csv', names=colnames)
    df['data']=df['data'].astype(str)

    #Il file che vado ad aprire serve per taggare tutti quei commit precedenti al commit con il primo tag associato, inoltre salvo lì la distanza della pub. versioni.
    #Questo perché è possibile che ci siano versioni precedenti della repo che hanno dei tag non associati correttamente a un commit (commit eliminato)
    colnames2=['tag','data']
    tagsdf= pd.read_csv(repopath+'/tags.csv', names=colnames2)
    tagsdf['data']=tagsdf['data'].astype(str)
    #nuovo: Serve per calcolare la media del tempo che intercorre tra due versioni, espresso in giorni
    tagsdf.at[0,'MediaTraVersioni']=-1
    df.at[0,'MediaTraCommit']=-1
    #fine nuovo
    #creo colonna vuota per la differenza di giorni tra i diversi tag
    tagsdf['differenza']=np.nan
    ver='0'
    #indice della riga nel file dei tag
    tagidx=1
    #Variabili per medie
    totGiorni=0
    totVersioni=0
    totCommit=0
    totGiorniCommit=0
    #reversed in modo da prenderli in ordine crescente di data
    for idx in reversed(df.index):
            #conversioni delle stringhe in date
            confrontoCommit=pd.to_datetime(df.at[idx, 'data'])
            #nuovo
            if(idx+1<len(df.index)):
                tempCommitattuale=pd.to_datetime(df.at[idx, 'data'][:-5])
                prossimoCommit=pd.to_datetime(df.at[idx+1, 'data'][:-5])
                totGiorniCommit+=abs((prossimoCommit-tempCommitattuale).days)
                totCommit+=1
            #finenuovo
            confrontoTagAttuale=pd.to_datetime(tagsdf.at[tagidx, 'data'])
            ver=tagsdf.at[tagidx,'tag']
            if(tagidx<len(tagsdf.index)-1):
                confrontoTagSuccessivo=pd.to_datetime(tagsdf.at[tagidx+1, 'data'])
                #se la data del commit è compresa tra il tag in analisi e il successivo
                if((confrontoTagAttuale<=confrontoCommit) & (confrontoTagSuccessivo>confrontoCommit)):
                    ver=tagsdf.at[tagidx,'tag']
                else:
                    if(confrontoTagSuccessivo<=confrontoCommit):
                        tagidx=tagidx+1
                        #contestualmente, calcolo e salvo la differenza di giorni tra un tag e l'altro, togliendo prima le timezione (approssimazione)
                        dataVecchia=pd.to_datetime(tagsdf.at[tagidx-1, 'data'][:-5])
                        dataNuova=pd.to_datetime(tagsdf.at[tagidx, 'data'][:-5])
                        tagsdf.at[tagidx, 'differenza']=abs((dataNuova-dataVecchia).days)
                        #aggiorno parametri per la media del tempo intercorso tra una versione e l'altra
                        totGiorni=abs((dataNuova-dataVecchia).days)+totGiorni
                        totVersioni=totVersioni+1
                        #commit appartiene ad una nuova versione, quindi lo flaggo come primo
                        ver=tagsdf.at[tagidx,'tag']+' - PRIMO'
            #questa assegnamento funziona in questo modo:
            #1- il commit ha data precedente al primo tag. Non posso dire a che versione appartengono, la segnalo con 0
            #2- il commit ha data successiva all'ultimo tag. La sua versione sarà quindi quella dell'ultimo tag
            #3- il commit si trova in uno stato "regolare", ovvero è compreso tra due tag x e x+1. Sarà taggato con x. PS. si può verificare anche il caso 2
            df.at[idx, 'versione']=ver

    print(totGiorni,' ',totVersioni)
    #Calcolo della media dei giorni trascorsi tra una versione e l'altra
    tagsdf.at[0,'MediaTraVersioni']=totGiorni/totVersioni
    df.at[0,'MediaTraCommit']=totGiorniCommit/totCommit

    tagsdf.to_csv(repopath+'/tags.csv', index=False)
    df.to_csv(repopath+'/commitsInfo.csv', index=False)

def updateFinalCsv(finalcsvpath,shpath,repopath,project_url,project_id):
    tagsdf= pd.read_csv(repopath+'/tags.csv')
    df = pd.read_csv(repopath+'/commitsInfo.csv')
    finaldf=pd.read_csv(finalcsvpath)
    finaldf['VersioneBuggy']=np.nan
    finaldf['VersioneFixed']=np.nan
    #NUOVO
    #Differenza di data tra versione buggata e versione fixata
    finaldf['DiffBugFix']=np.nan
    #Media della Differenza di data tra versione buggata e versione fixata
    finaldf['MediaBugFix']=np.nan
    #Numero totale delle versioni (tag)
    finaldf.at[0,'NumVersioni']=len(tagsdf.index)
    #Numero totale dei bug
    finaldf.at[0,'NumBug']=len(finaldf.index)
    #Media del tempo che intercorre tra una versione e l'altra, espressa in giorni
    finaldf.at[0, 'MediaCambioVersione']=tagsdf.at[0,'MediaTraVersioni']
    #Numero di commit
    finaldf.at[0, 'NumCommit']=len(df.index)-1
    #Media del tempo tra un commit e l'altro, espressa in ore
    finaldf.at[0,'MediaNuovoCommit']=df.at[0,'MediaTraCommit']
    finaldf.at[0,'MediaCommitPerVersione']=finaldf.at[0, 'NumCommit']/finaldf.at[0,'NumVersioni']

    finaldf['DiffBugFix']=finaldf['DiffBugFix'].astype(str)


    #FINE NUOVO
    finaldf['VersioneBuggy']=finaldf['VersioneBuggy'].astype(str)
    finaldf['VersioneFixed']=finaldf['VersioneFixed'].astype(str)

    #Somma delle differenze in termini di tempo tra versione buggata e versione fixata
    totbugfix=0
    #dovrebbe essere il numero dei bug, ma lo ricalcolo per evitare problemi
    nbugfix=0
    #contestualmente, aggiorno la versione nel csv finale
    contaVersioniBug=0
    contaVersioniFix=0
    for idx in (finaldf.index):
        #faccio differenza tra le date del buggy e del Fixed
        dataVecchia=pd.to_datetime(finaldf.at[idx, 'revision.date.buggy'][:-5])
        dataNuova=pd.to_datetime(finaldf.at[idx, 'revision.date.fixed'][:-5])
        finaldf.at[idx, 'DiffBugFix']=abs((dataNuova-dataVecchia).days)
        totbugfix+=abs((dataNuova-dataVecchia).days)
        nbugfix+=1

        #cerco il commit buggato nella lista dei commit
        foundBugged=df['commit'].str.contains(finaldf.at[idx,'revision.id.buggy'])
        rows=list(foundBugged[foundBugged==True].index)

        #print(rows)
        for row in rows:
            #finaldf.at[row,'DataBuggy']=df.at[idx,'data']
            finaldf.at[idx,'VersioneBuggy']=df.at[row,'versione']
            if contaVersioniBug==0:
                contaVersioniBug=1
            else:
                if((not finaldf.at[idx,'VersioneBuggy']==finaldf.at[idx-1,'VersioneBuggy'])& (not finaldf.at[idx,'VersioneBuggy']==finaldf.at[idx-1,'VersioneBuggy']+' - PRIMO')):
                    contaVersioniBug+=1
        foundFixed=df['commit'].str.contains(finaldf.at[idx,'revision.id.fixed'])
        rows=list(foundFixed[foundFixed==True].index)
        for row in rows:
            #finaldf.at[row,'DataFixed']=df.at[idx,'data']
            finaldf.at[idx,'VersioneFixed']=df.at[row,'versione']
            if contaVersioniFix==0:
                contaVersioniFix=1
            else:
                if((not finaldf.at[idx,'VersioneFixed']==finaldf.at[idx-1,'VersioneFixed'])& (not finaldf.at[idx,'VersioneFixed']==finaldf.at[idx-1,'VersioneFixed']+' - PRIMO')):
                    contaVersioniFix+=1


    print('Versioni buggate: ',contaVersioniBug,' Versioni fixate: ', contaVersioniFix)
    finaldf.at[0, 'MediaBugFix']=totbugfix/nbugfix
    df.to_csv(repopath+'/commitsInfo.csv', index=False)
    finaldf.to_csv(finalcsvpath, index=False)
