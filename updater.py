from time import sleep
import json
import os
import requests
from datetime import date
from dateutil.relativedelta import relativedelta
from heroCounters import analyze_replays

# date that is 1 month and 1 day old (data to be deleted)
old_day = (date.today() + relativedelta(months=-1,days=-1)).strftime('%Y-%m-%d')

dicName = 'dic_'+old_day
outName = 'stats_'+old_day+'.json'
# create & empty the dic and outfile files
open(dicName,'w').close()
open(outName,'w').close()
analyze_replays(beginPage=1,endPage=100,dicFileName=dicName,outFileName=outName,correct_day=old_day,one_day=True)
