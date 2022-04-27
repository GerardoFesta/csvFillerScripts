import pandas as pd

path_bugs='/home/gerardo/Scrivania/ver-comm-class/CLI_commitFileAggiornati.csv'
path_metrics='/home/gerardo/Scrivania/metricheSwAnalytics/CliMetrics.csv'
path_salvataggio='/home/gerardo/Scrivania/merged.csv'

bugsdf=pd.read_csv(path_bugs)
inhdf=pd.read_csv(path_metrics)
#Rimozione estensione .java dal file bugsdf
bugsdf['Classe']=bugsdf['Classe'].apply(lambda x: x[:-5])

merged=pd.merge(bugsdf,inhdf, how='right', on=['Classe','Commit'])

merged.to_csv(path_salvataggio,index=False)
