from pydriller import Repository
from pydriller import Commit
from pydriller import ModifiedFile

class SingleMiner:

    def getCommitInfo(repopath, commit):
        #ORIGINALE
        #repo=Repository(path_to_repo=repopath, single=commit).traverse_commits()

        #Nuovo
        repo=Repository(path_to_repo=repopath, single=commit, only_no_merge=True, only_in_branch='main').traverse_commits()

        #Il dizionario associerà alla chiave che rappresenta il nome del file, un dizionario interno che contiene tutti i dati di pydriller per quel file
        dict={}

        #Mock delle caratteristiche di un file non java modificato
        dizionario_finto={
            'nuovo':0,
            'eliminato':0,
            'modificato':0,
            'linee_aggiunte':0,
            'linee_rimosse':0,
            'nloc':0,
            'complexity':0,
            'token_count':0
        }
        #fine mock
        #Inserisco sempre 'altrifile' nel dizionario, in modo che ci sia per ogni commit nel fle csv finale
        dict['altrifile']=dizionario_finto
        #Esegue una sola volta
        for com in repo:

            files=com.modified_files
            print(commit)


            for file in files:
                if ".java" in file.filename:
                    innerdict={}
                    innerdict['nuovo']=0
                    #print(file.old_path)
                    if file.old_path is None:
                        innerdict['nuovo']=1

                    innerdict['eliminato']=0
                    if file.new_path is None:
                        innerdict['eliminato']=1
                    innerdict['modificato']=1
                    innerdict['linee_aggiunte']=file.added_lines
                    innerdict['linee_rimosse']=file.deleted_lines
                    innerdict['nloc']=file.nloc
                    innerdict['complexity']=file.complexity
                    innerdict['token_count']=file.token_count

                    #metti if ecc. new_path per percorso completo, filename per solo nome file
                    '''
                    if not file.new_path is None:
                        dict[file.new_path]=innerdict
                    else:
                        dict[file.old_path]=innerdict
                    '''
                    dict[file.filename]=innerdict
                else:
                    dizionario_finto['modificato']=1
                    dizionario_finto['linee_aggiunte']+=file.added_lines
                    dizionario_finto['linee_rimosse']+=file.deleted_lines
                    dict['altrifile']=dizionario_finto
        return dict
