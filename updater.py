from time import sleep
import json
import os
import requests
from datetime import date
from dateutil.relativedelta import relativedelta
from heroCounters import analyze_replays

# date that is 1 month and 1 week old (data to be deleted)
old_day = (date.today() + relativedelta(months=-1,weeks=-1)).strftime('%Y-%m-%d')
print "removing week from: " + old_day

oldDicName = 'dic_old_day_'+old_day
oldOutName = 'stats_old_day_'+old_day+'.json'
# create & empty the dic and outfile files
open(oldDicName,'w').close()
open(oldOutName,'w').close()
analyze_replays(beginPage=1,endPage=30,dicFileName=oldDicName,outFileName=oldOutName,correct_day=old_day,one_day=True)

# GOAL: Database updates every week
# Database is current with 1 month of data starting 1 month and 1 week ago
# Every week, grab new data (1 week long starting 2 weeks ago)
# Every week, delete old data (1 week long starting 1 month and 2 weeks ago)

# grab new data

start_date = (date.today() + relativedelta(weeks=-2)).strftime('%Y-%m-%d')
dicName = 'dic_new_data_'+start_date
outName = 'stats_new_data_'+start_date+'.json'
open(dicName,'w').close()
open(outName,'w').close()

analyze_replays(beginPage=1,endPage=30,dicFileName=dicName,outFileName=outName,correct_day=start_date,one_week=True)
