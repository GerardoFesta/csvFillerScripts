import pandas as pd

bugsdf=pd.read_csv('/home/gerardo/Scrivania/ver-comm-class/CLI_commitFileAggiornati.csv')
lista=[
'LOC',
'WMC',
'RFC',
'LCOM',
'CBO',
'DIT',
'NOC',
'impInh',
'intInh',
'delegations'
]
bugsdf['LOC']=""
bugsdf['WMC']=""
bugsdf['RFC']=""
bugsdf['LCOM']=""
bugsdf['CBO']=""
bugsdf['DIT']=""
bugsdf['NOC']=""
bugsdf['impInh']=""
bugsdf['intInh']=""
bugsdf['delegations']=""

inhdf=pd.read_csv('/home/gerardo/Scrivania/metricheSwAnalytics/metrics.csv')

for idx in inhdf.index:
    row=bugsdf.loc[(bugsdf['Commit']==inhdf.at[idx,'commit']) & (bugsdf['Classe']==inhdf.at[idx,'classe'])]
    row['LOC']=inhdf.at[idx,'LOC']
    row['WMC']=inhdf.at[idx,'WMC']
    row['RFC']=inhdf.at[idx,'RFC']
    row['LCOM']=inhdf.at[idx,'LCOM']
    row['CBO']=inhdf.at[idx,'CBO']
    row['DIT']=inhdf.at[idx,'DIT']
    row['NOC']=inhdf.at[idx,'NOC']
    row['impInh']=inhdf.at[idx,'impInh']
    row['intInh']=inhdf.at[idx,'intInh']
    row['delegations']=inhdf.at[idx,'delegations']

bugsdf.to_csv("/home/gerardo/Scrivania/merge.csv")
