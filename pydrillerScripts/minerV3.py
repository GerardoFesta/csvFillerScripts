from pydriller import Repository
from pydriller.metrics.process.change_set import ChangeSet
from pydriller.metrics.process.code_churn import CodeChurn
from pydriller.metrics.process.hunks_count import HunksCount


#con commit
class Miner:
    def mineVersion(repopath, lista):
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
        if(len(lista)==1):
            repo=Repository(path_to_repo=repopath, single=lista[0]).traverse_commits()
        else:
            repo=Repository(path_to_repo=repopath, only_commits=lista).traverse_commits()
        for commit in repo:

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

#        filesMetric= ChangeSet(path_to_repo=repopath, only_commits=lista)
#        maxFilesInCommit = filesMetric.max()
#        averageFilesInCommit = filesMetric.avg()

#        hunksMetric = HunksCount(path_to_repo=repopath, only_commits=lista)
#        hunks = hunksMetric.count()
#        totHunks=0
        #hunks è un dizionario dict
#        for a in hunks:
#            totHunks+=hunks.get(a)
#        totFile=len(hunks)


        returnVals={
            "linee_aggiunte": newLines,
            "linee_rimosse": delLines,
            "dmm_count": count_unit_size,
            "avg_dmm_unit_size": avg_dmm_unit_size,
            "avg_dmm_unit_complexity": avg_dmm_unit_complexity,
            "avg_dmm_unit_interfacing": avg_dmm_unit_interfacing,
            "max_files_in_commit": -1,
            "avg_files_in_commit": -1,
            "tot_hunks": -1,
            "tot_files_hunks": -1,
            "tot_commit": i
        }
        return returnVals
