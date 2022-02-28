import csv
import pandas as pd
import os
import subprocess
import numpy as np
from datetime import datetime, timezone
from minerV1 import Miner

class Feeder:

    def __init__(self,repo,csv,finalcsv):
        self.repo=repo
        self.csv=csv
        self.df = pd.read_csv(csv)
        self.finalcsv=finalcsv
        lista={'Versione':[],'Numero bug':[],'Numero fix':[],'Numero commit':[],'Tempo medio tra commit':[],'Tempo versione':[], 'Data inizio':[], 'Data fine':[], 'Linee aggiunte':[], 'Linee rimosse':[],'Numero Commit con DMM':[], 'Media DMM Unit Size':[], 'Media DMM Unit Complexity':[], 'Media DMM Unit Interfacing':[], 'Numero max file in commit':[], 'Numero media file in commit':[], 'Numero totale hunks':[], 'Numero file analizzati per hunks':[], 'Ncommit2':[]}
        self.finaldf=pd.DataFrame(lista)
        self.finaldf['Data inizio']=self.finaldf['Data inizio'].astype(str)
        self.finaldf['Data fine']=self.finaldf['Data fine'].astype(str)
        self.finaldf['Versione']=self.finaldf['Versione'].astype(str)

    def feed(self):
        print(self.finalcsv)
        for idx in self.df.index:
            self.finaldf.at[idx, "Versione"]=self.df.at[idx,"Versione"]
            self.finaldf.at[idx, "Numero bug"]=self.df.at[idx,"Numero bug"]
            self.finaldf.at[idx, "Numero fix"]=self.df.at[idx,"Numero fix"]
            self.finaldf.at[idx, "Numero commit"]=self.df.at[idx,"Numero commit"]
            self.finaldf.at[idx, "Tempo medio tra commit"]=self.df.at[idx,"Tempo medio tra commit"]
            self.finaldf.at[idx, "Tempo versione"]=self.df.at[idx,"Tempo versione"]
            self.finaldf.at[idx, "Data inizio"]=self.df.at[idx,"Data inizio"]
            self.finaldf.at[idx, "Data fine"]=self.df.at[idx,"Data fine"]
            print(self.df.at[idx,"Versione"])
            risultati_versione=Miner.mineVersion(self.repo, self.df.at[idx,"Primo commit"], self.df.at[idx,"Ultimo commit"])

            self.finaldf.at[idx,"Linee aggiunte"]=risultati_versione.get("linee_aggiunte")
            self.finaldf.at[idx,"Linee rimosse"]=risultati_versione.get("linee_rimosse")
            self.finaldf.at[idx,"Numero Commit con DMM"]=risultati_versione.get("dmm_count")
            self.finaldf.at[idx,"Media DMM Unit Size"]=risultati_versione.get("avg_dmm_unit_size")
            self.finaldf.at[idx,"Media DMM Unit Complexity"]=risultati_versione.get("avg_dmm_unit_complexity")
            self.finaldf.at[idx,"Media DMM Unit Interfacing"]=risultati_versione.get("avg_dmm_unit_interfacing")
            self.finaldf.at[idx,"Numero max file in commit"]=risultati_versione.get("max_files_in_commit")
            self.finaldf.at[idx,"Numero media file in commit"]=risultati_versione.get("avg_files_in_commit")
            self.finaldf.at[idx,"Numero totale hunks"]=risultati_versione.get("tot_hunks")
            self.finaldf.at[idx,"Numero file analizzati per hunks"]=risultati_versione.get("tot_files_hunks")
            self.finaldf.at[idx,"Ncommit2"]=risultati_versione.get("tot_commit")
        print("salvo")
        self.finaldf.to_csv(self.finalcsv, index=False)
        print("salvato")
