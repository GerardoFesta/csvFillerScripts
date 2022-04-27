from pydriller import Repository
from pydriller.metrics.process.change_set import ChangeSet
from pydriller.metrics.process.code_churn import CodeChurn
from pydriller.metrics.process.hunks_count import HunksCount
import datetime

#con date
class Miner:
    def mineVersion(repopath, startCommit, endCommit):
        i=0
        newLines=0
        delLines=0
        count_unit_size=0
        sum_unit_size=0
        count_unit_complexity=0
        sum_unit_complexity=0
        count_unit_interfacing=0
        sum_unit_interfacing=0
        avg_dmm_unit_size=-1
        avg_dmm_unit_complexity=-1
        avg_dmm_unit_interfacing=-1
        if(startCommit==endCommit):
            repo=Repository(path_to_repo=repopath, single=startCommit).traverse_commits()
        else:
            repo=Repository(path_to_repo=repopath, since=startCommit, to=endCommit).traverse_commits()
        for commit in repo:
            #print(commit.hash)
            i+=1
            newLines+=commit.insertions
            delLines+=commit.deletions
            if(not commit.dmm_unit_size==None):
                count_unit_size+=1
                sum_unit_size+=commit.dmm_unit_size
            if(not commit.dmm_unit_complexity==None):
                count_unit_complexity+=1
                sum_unit_complexity+=commit.dmm_unit_complexity
            if(not commit.dmm_unit_interfacing==None):
                count_unit_interfacing+=1
                sum_unit_interfacing+=commit.dmm_unit_interfacing

        if(not count_unit_size==0): avg_dmm_unit_size=sum_unit_size/count_unit_size
        if(not count_unit_complexity==0): avg_dmm_unit_complexity=sum_unit_complexity/count_unit_complexity
        if(not count_unit_interfacing==0): avg_dmm_unit_interfacing=sum_unit_interfacing/count_unit_interfacing

        filesMetric= ChangeSet(path_to_repo=repopath, since=startCommit, to=endCommit)
        maxFilesInCommit = filesMetric.max()
        averageFilesInCommit = filesMetric.avg()

        hunksMetric = HunksCount(path_to_repo=repopath, since=startCommit, to=endCommit)
        hunks = hunksMetric.count()
        totHunks=0
        #hunks è un dizionario dict
        for a in hunks:
            totHunks+=hunks.get(a)
        totFile=len(hunks)


        returnVals={
            "linee_aggiunte": newLines,
            "linee_rimosse": delLines,
            "dmm_count": count_unit_size,
            "avg_dmm_unit_size": avg_dmm_unit_size,
            "avg_dmm_unit_complexity": avg_dmm_unit_complexity,
            "avg_dmm_unit_interfacing": avg_dmm_unit_interfacing,
            "max_files_in_commit": maxFilesInCommit,
            "avg_files_in_commit": averageFilesInCommit,
            "tot_hunks": totHunks,
            "tot_files_hunks": totFile,
            "tot_commit": i
        }
        print(i)
        return returnVals
'''
d1=datetime.datetime.strptime("2009-03-16 07:26:44 +0000", "%Y-%m-%d %H:%M:%S %z")
d2=datetime.datetime.strptime("2009-03-16 07:29:19 +0000", "%Y-%m-%d %H:%M:%S %z")
dict=Miner.mineVersion("/home/gerardo/VersioniCli/Cli", d1,d2)

print(dict["tot_commit"])
'''
