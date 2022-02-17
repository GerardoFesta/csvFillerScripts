import csv
import pandas as pd
import os
import subprocess
import numpy as np
from datetime import datetime, timezone



def getBugsFixesNumber(revisionpath,finalcsvpath,shpath,repopath,project_url,project_id):
    df = pd.read_csv(revisionpath)
    finaldf=pd.read_csv(finalcsvpath)

    for idx in finaldf.index:
        contabug=len(df.loc[df['VersioneBuggy']==finaldf.at[idx,'Versione']].index)
        nuovastringa=''
        if ' - PRIMO' in finaldf.at[idx, 'Versione']:
            nuovastringa=finaldf.at[idx,'Versione'][:-8]
        else:
            nuovastringa=finaldf.at[idx,'Versione']+' - PRIMO'

        contabug+=len(df.loc[df['VersioneBuggy']==nuovastringa].index)

        contafixed=len(df.loc[df['VersioneFixed']==finaldf.at[idx,'Versione']].index)
        contafixed+=len(df.loc[df['VersioneFixed']==nuovastringa].index)
        finaldf.at[idx, 'Numero bug']=contabug
        finaldf.at[idx, 'Numero fix']=contafixed

    finaldf.to_csv(finalcsvpath, index=False)


def getInfo(revisionpath,finalcsvpath,shpath,repopath,project_url,project_id):
    colnames=['commit', 'data', 'versione','ex1','ex2','ex3','MediaTraCommit']
    df = pd.read_csv(repopath+'/commitsInfo.csv', names=colnames)
    df['data']=df['data'].astype(str)

    lista={'Versione':[], 'Primo commit':[],'Ultimo commit':[],'Numero bug':[],'Numero fix':[],'Numero commit':[],'Tempo medio tra commit':[],'Tempo versione':[], 'Data inizio':[], 'Data fine':[]}
    finaldf=pd.DataFrame(lista)
    finaldf.at[0,'Data inizio']=0

    finaldf['Data inizio']=finaldf['Data inizio'].astype(str)
    finaldf['Data fine']=finaldf['Data fine'].astype(str)
    finaldf['Versione']=finaldf['Versione'].astype(str)
    finaldf['Primo commit']=finaldf['Primo commit'].astype(str)
    finaldf['Ultimo commit']=finaldf['Ultimo commit'].astype(str)

    finalidx=0
    contacommit=0
    totTempoCommit=0

    for idx in reversed(df.index):

        if(idx==len(df.index)-1):
            finaldf.at[finalidx,'Versione']=df.at[idx,'versione']
            finaldf.at[finalidx,'Primo commit']=df.at[idx,'commit']
            finaldf.at[finalidx, 'Data inizio']=df.at[idx,'data']
            contacommit+=1

        if((not idx<=1)and(not idx==len(df.index)-1)and(not df.at[idx,'versione']==df.at[idx+1,'versione'])&(not (df.at[idx,'versione']+' - PRIMO')==(df.at[idx+1,'versione']))):

            finalidx+=1
            finaldf.at[finalidx,'Versione']=df.at[idx,'versione']
            finaldf.at[finalidx,'Primo commit']=df.at[idx,'commit']
            finaldf.at[finalidx, 'Data inizio']=df.at[idx,'data']

            finaldf.at[finalidx-1,'Ultimo commit']=df.at[idx+1,'commit']
            finaldf.at[finalidx-1, 'Data fine']=df.at[idx+1,'data']

            data1=pd.to_datetime(finaldf.at[finalidx-1, 'Data inizio'][:-5])
            data2=pd.to_datetime(finaldf.at[finalidx-1, 'Data fine'][:-5])
            finaldf.at[finalidx-1,'Tempo versione']=abs((data1-data2).days)
            finaldf.at[finalidx-1,'Numero commit']=contacommit
            finaldf.at[finalidx-1,'Tempo medio tra commit']=finaldf.at[finalidx-1,'Tempo versione']/finaldf.at[finalidx-1,'Numero commit']
            totTempoCommit=0
            contacommit=1


        if((not idx<=1) and(not idx==len(df.index)-1)):
            if((df.at[idx,'versione']==df.at[idx+1,'versione']) or (df.at[idx,'versione']+' - PRIMO'==df.at[idx+1,'versione'])):
                contacommit+=1
                data1=pd.to_datetime(df.at[idx, 'data'][:-5])
                data2=pd.to_datetime(df.at[idx+1, 'data'][:-5])
                totTempoCommit+=abs((data1-data2).days)

        if((idx==1) and ((df.at[idx,'versione']==df.at[idx+1,'versione'])or (df.at[idx,'versione']+' - PRIMO'==df.at[idx+1,'versione']))):
            contacommit+=1
            data1=pd.to_datetime(df.at[idx, 'data'][:-5])
            data2=pd.to_datetime(df.at[idx+1, 'data'][:-5])
            totTempoCommit+=abs((data1-data2).days)
            finaldf.at[finalidx,'Ultimo commit']=df.at[idx,'commit']
            finaldf.at[finalidx, 'Data fine']=df.at[idx,'data']
            data1=pd.to_datetime(finaldf.at[finalidx, 'Data inizio'][:-5])
            data2=pd.to_datetime(finaldf.at[finalidx, 'Data fine'][:-5])
            finaldf.at[finalidx,'Tempo versione']=abs((data1-data2).days)
            finaldf.at[finalidx,'Numero commit']=contacommit
            finaldf.at[finalidx,'Tempo medio tra commit']=finaldf.at[finalidx,'Tempo versione']/finaldf.at[finalidx,'Numero commit']

    finaldf.to_csv(finalcsvpath, index=False)

    getBugsFixesNumber(revisionpath,finalcsvpath,shpath,repopath,project_url,project_id)


def cli():
    finalcsvpath='/home/gerardo/Scrivania/AnalisiVersioni/CliVersions.csv'
    revisionpath='/home/gerardo/Scrivania/revisions/CliRevisions.csv'
    shpath='/home/gerardo/Scrivania/csvFillerScripts/AllVersionsScripts/'
    repopath='/home/gerardo/VersioniCli/Cli'
    project_url='https://github.com/apache/commons-cli'
    project_id='Cli'
    getInfo(revisionpath,finalcsvpath,shpath,repopath,project_url,project_id)

def closurecompiler():
    finalcsvpath='/home/gerardo/Scrivania/AnalisiVersioni/ClosureVersions.csv'
    revisionpath='/home/gerardo/Scrivania/revisions/ClosureRevisions.csv'
    shpath='/home/gerardo/Scrivania/csvFillerScripts/AllVersionsScripts/'
    repopath='/home/gerardo/VersioniClosure/Closure'
    project_url='https://github.com/google/closure-compiler'
    project_id='Closure'
    getInfo(revisionpath,finalcsvpath,shpath,repopath,project_url,project_id)

def commonsCodec():
    finalcsvpath='/home/gerardo/Scrivania/AnalisiVersioni/CodecVersions.csv'
    revisionpath='/home/gerardo/Scrivania/revisions/CodecRevisions.csv'
    shpath='/home/gerardo/Scrivania/csvFillerScripts/AllVersionsScripts/'
    repopath='/home/gerardo/VersioniCodec/Codec'
    project_url='https://github.com/apache/commons-codec'
    project_id='Codec'
    getInfo(revisionpath,finalcsvpath,shpath,repopath,project_url,project_id)

def commonsCollection():
    finalcsvpath='/home/gerardo/Scrivania/AnalisiVersioni/CollectionsVersions.csv'
    revisionpath='/home/gerardo/Scrivania/revisions/CollectionsRevisions.csv'
    shpath='/home/gerardo/Scrivania/csvFillerScripts/AllVersionsScripts/'
    repopath='/home/gerardo/VersioniCollections/Collections'
    project_url='https://github.com/apache/commons-collections'
    project_id='Collections'
    getInfo(revisionpath,finalcsvpath,shpath,repopath,project_url,project_id)

def commonsCSV():
    finalcsvpath='/home/gerardo/Scrivania/AnalisiVersioni/commons-csvVersions.csv'
    revisionpath='/home/gerardo/Scrivania/revisions/commons-csvrevisions.csv'
    shpath='/home/gerardo/Scrivania/csvFillerScripts/AllVersionsScripts/'
    repopath='/home/gerardo/VersioniCommons-csv/commons-csv'
    project_url='https://github.com/apache/commons-csv'
    project_id='Csv'
    getInfo(revisionpath,finalcsvpath,shpath,repopath,project_url,project_id)

def compress():
    finalcsvpath='/home/gerardo/Scrivania/AnalisiVersioni/CompressVersions.csv'
    revisionpath='/home/gerardo/Scrivania/revisions/CompressRevisions.csv'
    shpath='/home/gerardo/Scrivania/csvFillerScripts/AllVersionsScripts/'
    repopath='/home/gerardo/VersioniCompress/Compress'
    project_url='https://github.com/apache/commons-compress'
    project_id='Compress'
    getInfo(revisionpath,finalcsvpath,shpath,repopath,project_url,project_id)

def gson():
    finalcsvpath='/home/gerardo/Scrivania/AnalisiVersioni/GsonVersions.csv'
    revisionpath='/home/gerardo/Scrivania/revisions/GsonRevisions.csv'
    shpath='/home/gerardo/Scrivania/csvFillerScripts/AllVersionsScripts/'
    repopath='/home/gerardo/VersioniGson/Gson'
    project_url='https://github.com/google/gson'
    project_id='Gson'
    getInfo(revisionpath,finalcsvpath,shpath,repopath,project_url,project_id)

def jacksonCore():
    finalcsvpath='/home/gerardo/Scrivania/AnalisiVersioni/jackson-coreVersions.csv'
    revisionpath='/home/gerardo/Scrivania/revisions/jackson-corerevisions.csv'
    shpath='/home/gerardo/Scrivania/csvFillerScripts/AllVersionsScripts/'
    repopath='/home/gerardo/VersioniJackson-core/jackson-core'
    project_url='https://github.com/FasterXML/jackson-core'
    project_id='JacksonCore'
    getInfo(revisionpath,finalcsvpath,shpath,repopath,project_url,project_id)

def jacksonDatabind():
    finalcsvpath='/home/gerardo/Scrivania/AnalisiVersioni/JacksonDatabindVersions.csv'
    revisionpath='/home/gerardo/Scrivania/revisions/JacksonDatabindRevisions.csv'
    shpath='/home/gerardo/Scrivania/csvFillerScripts/AllVersionsScripts/'
    repopath='/home/gerardo/VersioniJacksonDatabind/JacksonDatabind'
    project_url='https://github.com/FasterXML/jackson-databind'
    project_id='JacksonDatabind'
    getInfo(revisionpath,finalcsvpath,shpath,repopath,project_url,project_id)

def jacksonXml():
    finalcsvpath='/home/gerardo/Scrivania/AnalisiVersioni/JacksonXmlVersions.csv'
    revisionpath='/home/gerardo/Scrivania/revisions/JacksonXmlRevisions.csv'
    shpath='/home/gerardo/Scrivania/csvFillerScripts/AllVersionsScripts/'
    repopath='/home/gerardo/VersioniJacksonXml/JacksonXml'
    project_url='https://github.com/FasterXML/jackson-dataformat-xml'
    project_id='JacksonXml'
    getInfo(revisionpath,finalcsvpath,shpath,repopath,project_url,project_id)

def jsoup():
    finalcsvpath='/home/gerardo/Scrivania/AnalisiVersioni/jsoupVersions.csv'
    revisionpath='/home/gerardo/Scrivania/revisions/newjsoup_revisions.csv'
    shpath='/home/gerardo/Scrivania/csvFillerScripts/AllVersionsScripts/'
    repopath='/home/gerardo/VersioniJsoup/jsoup'
    project_url='https://github.com/jhy/jsoup'
    project_id='Jsoup'
    getInfo(revisionpath,finalcsvpath,shpath,repopath,project_url,project_id)

def jxPath():
    finalcsvpath='/home/gerardo/Scrivania/AnalisiVersioni/JxPathVersions.csv'
    revisionpath='/home/gerardo/Scrivania/revisions/JxPathRevisions.csv'
    shpath='/home/gerardo/Scrivania/csvFillerScripts/AllVersionsScripts/'
    repopath='/home/gerardo/VersioniJxPath/JxPath'
    project_url='https://github.com/apache/commons-jxpath'
    project_id='JxPath'
    getInfo(revisionpath,finalcsvpath,shpath,repopath,project_url,project_id)

def mockito():
    finalcsvpath='/home/gerardo/Scrivania/AnalisiVersioni/MockitoVersions.csv'
    revisionpath='/home/gerardo/Scrivania/revisions/Mockitoevisions.csv'
    shpath='/home/gerardo/Scrivania/csvFillerScripts/AllVersionsScripts/'
    repopath='/home/gerardo/VersioniMockito/Mockito'
    project_url='https://github.com/mockito/mockito'
    project_id='Mockito'
    getInfo(revisionpath,finalcsvpath,shpath,repopath,project_url,project_id)

def time():
    finalcsvpath='/home/gerardo/Scrivania/AnalisiVersioni/TimeVersions.csv'
    revisionpath='/home/gerardo/Scrivania/revisions/TimeRevisions.csv'
    shpath='/home/gerardo/Scrivania/csvFillerScripts/AllVersionsScripts/'
    repopath='/home/gerardo/VersioniTime/Time'
    project_url='https://github.com/JodaOrg/joda-time'
    project_id='Time'
    getInfo(revisionpath,finalcsvpath,shpath,repopath,project_url,project_id)







cli()
closurecompiler()
commonsCodec()
commonsCollection()
commonsCSV()
compress()
gson()
jacksonCore()
jacksonDatabind()
jacksonXml()
jsoup()
jxPath()
mockito()
time()
