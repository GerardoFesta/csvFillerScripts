import csv
import pandas as pd
import os
import subprocess
import numpy as np
from datetime import datetime, timezone
import FillerScripts
# defects4j query -H -p Jsoup -q "bug.id,revision.id.buggy,revision.id.fixed,report.id,report.url,revision.date.buggy,revision.date.fixed" -o aaaaaaaaaaaaa.csv
finalcsvpath='/home/gerardo/Scrivania/revisions/JacksonDatabindRevisions.csv'
shpath='/home/gerardo/Scrivania/csvFillerScripts/'
repopath='/home/gerardo/VersioniJacksonDatabind/JacksonDatabind'
project_url='https://github.com/FasterXML/jackson-databind'
project_id='JacksonDatabind'


FillerScripts.cloneProject(finalcsvpath,shpath,repopath,project_url,project_id)
FillerScripts.getD4jInfo(finalcsvpath,shpath,repopath,project_url,project_id)
FillerScripts.getCommitsVersionsDate(finalcsvpath,shpath,repopath,project_url,project_id)
FillerScripts.updateFinalCsv(finalcsvpath,shpath,repopath,project_url,project_id)
