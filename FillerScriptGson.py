import csv
import pandas as pd
import os
import subprocess
import numpy as np
from datetime import datetime, timezone
import FillerScripts
# defects4j query -H -p Jsoup -q "bug.id,revision.id.buggy,revision.id.fixed,report.id,report.url,revision.date.buggy,revision.date.fixed" -o aaaaaaaaaaaaa.csv
finalcsvpath='/home/gerardo/Scrivania/revisions/GsonRevisions.csv'
shpath='/home/gerardo/Scrivania/csvFillerScripts/'
repopath='/home/gerardo/VersioniGson/Gson'
project_url='https://github.com/google/gson'
project_id='Gson'


FillerScripts.cloneProject(finalcsvpath,shpath,repopath,project_url,project_id)
FillerScripts.getD4jInfo(finalcsvpath,shpath,repopath,project_url,project_id)
FillerScripts.getCommitsVersionsDate(finalcsvpath,shpath,repopath,project_url,project_id)
FillerScripts.updateFinalCsv(finalcsvpath,shpath,repopath,project_url,project_id)
