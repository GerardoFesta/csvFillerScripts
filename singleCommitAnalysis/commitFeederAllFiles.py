import pandas as pd
from singleCommitMiner import SingleMiner


class Feeder:

    def __init__(self,repo,commitscsv, finalcsv, bugscsv):
        self.repo=repo
        self.df = pd.read_csv(commitscsv)
        lista={'Versione':[],'Commit':[],'Classe':[],'Bug':[],'Fix':[],'Modificata':[], 'Esistente':[], 'Creato':[], 'Eliminato':[], 'Linee aggiunte':[],'Linee rimosse':[], 'Nloc':[], 'Complexity':[], 'Token count':[]}
        self.finalcsvpath=finalcsv
        self.finaldf=pd.DataFrame(lista)
        self.bugsdf=pd.read_csv(bugscsv)

        #Modifica se cambi tipologia di file (path completo o solo nome file)
        path_file=repo+'/tuttifile.txt'
        file1 = open(path_file, 'r')
        Lines = file1.readlines()


        self.lista_file=[]
        self.file_esistenti={}
        self.file_eliminati={}
        for line in Lines:
            file=line.strip()
            self.lista_file.append(file)
            self.file_esistenti[file]=0
            self.file_eliminati[file]=0


    def feed(self):
        #MOCK PER TEST
        #self.finaldf=pd.read_csv(self.finalcsvpath)
        #FINE MOCK

            #reversed da più vecchio a più recente
            for idx in reversed(self.df.index):
                dict=SingleMiner.getCommitInfo(self.repo, self.df.at[idx,'commit'])

                fissa={'Versione':self.df.at[idx,'versione'], 'Commit':self.df.at[idx,'commit']}
                #FILE MODIFICATI DAL SINGOLO COMMIT
                for classe in dict:
                    inner=dict[classe]
                    self.file_eliminati[classe]=inner['eliminato']
                    #Se lo modifico esiste già o al più lo creo in questo commit
                    self.file_esistenti[classe]=1
                    if inner['eliminato']==1:
                        self.file_esistenti[classe]=0
                    riga={'Classe':classe,'Bug':0,'Fix':0,'Modificata':inner['modificato'], 'Esistente':self.file_esistenti[classe], 'Creato':inner['nuovo'], 'Eliminato':inner['eliminato'], 'Linee aggiunte':inner['linee_aggiunte'],'Linee rimosse':inner['linee_rimosse'], 'Nloc':inner['nloc'], 'Complexity':inner['complexity'], 'Token count':inner['token_count']}
                    merge=fissa|riga
                    self.finaldf=self.finaldf.append(merge, ignore_index=True)

                #ALTRI FILE NON MODIFICATI DAL COMMIT
                file_modificati=set(dict.keys())
                non_modificati=list(set(self.file_esistenti)-file_modificati)
                for classe in non_modificati:
                    riga={'Classe':classe,'Bug':0,'Fix':0,'Modificata':0, 'Esistente':self.file_esistenti[classe], 'Creato':0, 'Eliminato':0, 'Linee aggiunte':0,'Linee rimosse':0, 'Nloc':0, 'Complexity':0, 'Token count':0}
                    merge=fissa|riga
                    self.finaldf=self.finaldf.append(merge, ignore_index=True)

            self.finaldf.to_csv(self.finalcsvpath, index=False)

    def buggedClassesSpotter(self, com_bug, com_fix):
        lista_bug=SingleMiner.getCommitInfo(self.repo, com_bug)
        lista_fix=SingleMiner.getCommitInfo(self.repo, com_fix)
        '''
            print("--------------------------------------------------------------")
            print('buggato: ', com_bug)
            print('fixato: ', com_fix)
            print(lista_bug.keys())
            print(lista_fix.keys())


        '''
        return lista_bug.keys(), lista_fix.keys()

    def bugFixFiller(self):
        #self.finaldf.loc[self.finaldf['Modificata']==0, 'Modificata']=1

        for idx in self.bugsdf.index:
            buggato=self.bugsdf.at[idx,'revision.id.buggy']
            fixato=self.bugsdf.at[idx,'revision.id.fixed']
            classibuggate, classifixate=Feeder.buggedClassesSpotter(self,buggato,fixato)
            self.finaldf.loc[(self.finaldf['Commit']==buggato) & (self.finaldf['Classe'].isin(classibuggate)), 'Bug']+=1
            self.finaldf.loc[(self.finaldf['Commit']==fixato) & (self.finaldf['Classe'].isin(classifixate)), 'Fix']+=1

            self.finaldf.to_csv(self.finalcsvpath, index=False)
            print("salvo", self.finalcsvpath)
            '''
                classibuggate=Feeder.buggedClassesSpotter(self,buggato,fixato)
                print(self.finaldf.loc[(self.finaldf['Commit']==buggato) & (self.finaldf['Classe'].isin(classibuggate))])
            '''



#feeder=Feeder("/home/gerardo/VersioniCollections/Collections", "/home/gerardo/VersioniCollections/Collections/commitsInfo.csv", "/home/gerardo/Scrivania/ver-comm-class/COLLECTIONS_commitFileAggiornati.csv", "/home/gerardo/Scrivania/revisions/CollectionsRevisions.csv")
#feeder.feed()
#feeder.bugFixFiller()
feeder=Feeder("/home/gerardo/VersioniCommons-csv/commons-csv", "/home/gerardo/VersioniCommons-csv/commons-csv/commitsInfo.csv", "/home/gerardo/Scrivania/ver-comm-class/COMMONS-CSV_commitFileAggiornati.csv", "/home/gerardo/Scrivania/revisions/commons-csvrevisions.csv")
feeder.feed()
feeder.bugFixFiller()
#feeder=Feeder("/home/gerardo/VersioniCompress/Compress", "/home/gerardo/VersioniCompress/Compress/commitsInfo.csv", "/home/gerardo/Scrivania/ver-comm-class/COMPRESS_commitFileAggiornati.csv", "/home/gerardo/Scrivania/revisions/CompressRevisions.csv")
#feeder.feed()
#feeder.bugFixFiller()
feeder=Feeder("/home/gerardo/VersioniJackson-core/jackson-core", "/home/gerardo/VersioniJackson-core/jackson-core/commitsInfo.csv", "/home/gerardo/Scrivania/ver-comm-class/JACKSON-CORE_commitFileAggiornati.csv", "/home/gerardo/Scrivania/revisions/jackson-corerevisions.csv")
feeder.feed()
feeder.bugFixFiller()
#feeder=Feeder("/home/gerardo/VersioniJacksonDatabind/JacksonDatabind", "/home/gerardo/VersioniJacksonDatabind/JacksonDatabind/commitsInfo.csv", "/home/gerardo/Scrivania/ver-comm-class/JACKSON-DATABIND_commitFileAggiornati.csv", "/home/gerardo/Scrivania/revisions/JacksonDatabindRevisions.csv")
#feeder.feed()
#feeder.bugFixFiller()
feeder=Feeder("/home/gerardo/VersioniJacksonXml/JacksonXml", "/home/gerardo/VersioniJacksonXml/JacksonXml/commitsInfo.csv", "/home/gerardo/Scrivania/ver-comm-class/JACKSON-XML_commitFileAggiornati.csv", "/home/gerardo/Scrivania/revisions/JacksonXmlRevisions.csv")
feeder.feed()
feeder.bugFixFiller()
feeder=Feeder("/home/gerardo/VersioniJxPath/JxPath", "/home/gerardo/VersioniJxPath/JxPath/commitsInfo.csv", "/home/gerardo/Scrivania/ver-comm-class/JX-PATH_commitFileAggiornati.csv", "/home/gerardo/Scrivania/revisions/JxPathRevisions.csv")
feeder.feed()
feeder.bugFixFiller()
#feeder=Feeder("/home/gerardo/VersioniMockito/Mockito", "/home/gerardo/VersioniMockito/Mockito/commitsInfo.csv", "/home/gerardo/Scrivania/ver-comm-class/MOCKITO_commitFileAggiornati.csv", "/home/gerardo/Scrivania/revisions/Mockitoevisions.csv")
#feeder.feed()
#feeder.bugFixFiller()
feeder=Feeder("/home/gerardo/VersioniTime/Time", "/home/gerardo/VersioniTime/Time/commitsInfo.csv", "/home/gerardo/Scrivania/ver-comm-class/TIME_commitFileAggiornati.csv", "/home/gerardo/Scrivania/revisions/TimeRevisions.csv")
feeder.feed()
feeder.bugFixFiller()
print("fine")
