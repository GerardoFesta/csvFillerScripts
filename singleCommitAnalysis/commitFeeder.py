import pandas as pd
from singleCommitMiner import SingleMiner

#IL CAMPO ESISTENTE E' PLACEHOLDER

class Feeder:

    def __init__(self,repo,commitscsv, finalcsv, bugscsv):
        self.repo=repo
        self.df = pd.read_csv(commitscsv)
        lista={'Versione':[],'Commit':[],'Classe':[],'Bug':[],'Fix':[],'Modificata':[], 'Esistente':[], 'Creato':[], 'Eliminato':[], 'Linee aggiunte':[],'Linee rimosse':[], 'Nloc':[], 'Complexity':[], 'Token count':[]}
        self.finalcsvpath=finalcsv
        self.finaldf=pd.DataFrame(lista)
        self.bugsdf=pd.read_csv(bugscsv)


    def feed(self):
        #MOCK PER TEST
        self.finaldf=pd.read_csv(self.finalcsvpath)
        #FINE MOCK
        '''
            for idx in self.df.index:
                dict=SingleMiner.getCommitInfo(self.repo, self.df.at[idx,'commit'])

                fissa={'Versione':self.df.at[idx,'versione'], 'Commit':self.df.at[idx,'commit']}
                for classe in dict:
                    inner=dict[classe]
                    riga={'Classe':classe,'Bug':0,'Fix':0,'Modificata':1, 'Esistente':1, 'Creato':inner['nuovo'], 'Eliminato':inner['eliminato'], 'Linee aggiunte':inner['linee_aggiunte'],'Linee rimosse':inner['linee_rimosse'], 'Nloc':inner['nloc'], 'Complexity':inner['complexity'], 'Token count':inner['token_count']}
                    merge=fissa|riga
                    self.finaldf=self.finaldf.append(merge, ignore_index=True)


            self.finaldf.to_csv(self.finalcsvpath, index=False)
        '''

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
            self.finaldf.loc[(self.finaldf['Commit']==buggato) & (self.finaldf['Classe'].isin(classibuggate)), 'Bug']=1
            self.finaldf.loc[(self.finaldf['Commit']==fixato) & (self.finaldf['Classe'].isin(classifixate)), 'Fix']=1

            self.finaldf.to_csv(self.finalcsvpath, index=False)
            '''
                classibuggate=Feeder.buggedClassesSpotter(self,buggato,fixato)
                print(self.finaldf.loc[(self.finaldf['Commit']==buggato) & (self.finaldf['Classe'].isin(classibuggate))])
            '''



feeder=Feeder("/home/gerardo/VersioniCli/Cli", "/home/gerardo/VersioniCli/Cli/commitsInfo.csv", "/home/gerardo/Scrivania/provaTuttiCommitClassiCLI.csv", "/home/gerardo/Scrivania/revisions/CliRevisions.csv")
feeder.feed()
feeder.bugFixFiller()
