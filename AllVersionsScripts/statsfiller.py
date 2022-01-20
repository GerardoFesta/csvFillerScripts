import csv
import pandas as pd
import os
import subprocess
import numpy as np
from datetime import datetime, timezone

nomicsv=['/home/gerardo/Scrivania/revisions/CliRevisions.csv', '/home/gerardo/Scrivania/revisions/ClosureRevisions.csv',
'/home/gerardo/Scrivania/revisions/CodecRevisions.csv','/home/gerardo/Scrivania/revisions/CollectionsRevisions.csv','/home/gerardo/Scrivania/revisions/commons-csvrevisions.csv','/home/gerardo/Scrivania/revisions/CompressRevisions.csv','/home/gerardo/Scrivania/revisions/GsonRevisions.csv','/home/gerardo/Scrivania/revisions/jackson-corerevisions.csv','/home/gerardo/Scrivania/revisions/JacksonDatabindRevisions.csv',
'/home/gerardo/Scrivania/revisions/JacksonXmlRevisions.csv','/home/gerardo/Scrivania/revisions/newjsoup_revisions.csv','/home/gerardo/Scrivania/revisions/JxPathRevisions.csv','/home/gerardo/Scrivania/revisions/LangRevisions.csv','/home/gerardo/Scrivania/revisions/MathRevisions.csv', '/home/gerardo/Scrivania/revisions/Mockitoevisions.csv', '/home/gerardo/Scrivania/revisions/TimeRevisions.csv' ]

df = pd.read_csv('/home/gerardo/Scrivania/Medie.csv')
i=0
for idx in nomicsv:

    secondodf=pd.read_csv(idx)
    df.at[i,'Numero Bug']=round(secondodf.at[0,'NumBug'])
    df.at[i,'Media Giorni per fixare bug']=round(secondodf.at[0,'MediaBugFix'])
    df.at[i,'Numero totale di versioni']=round(secondodf.at[0,'NumVersioni'])
    df.at[i,'Media giorni per cambio versione']=round(secondodf.at[0,'MediaCambioVersione'])
    df.at[i,'Numero totale di commit']=round(secondodf.at[0,'NumCommit'])
    df.at[i,'Media di commit per versione']=round(secondodf.at[0,'MediaCommitPerVersione'])
    df.at[i,'Media giorni per nuovo commit']=round(secondodf.at[0,'MediaNuovoCommit'])
    i=i+1


print(df)
df.to_csv('/home/gerardo/Scrivania/Medie.csv', index=False)
