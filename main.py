import json
import requests
from datetime import date
from dateutil.relativedelta import relativedelta
from time import sleep
from heroCounters import analyze_replays


start_date=(date.today()+relativedelta(months=-1,weeks=-1)).strftime('%Y-%m-%d')
print "Analyzing 1 Month of Replays starting from: " + start_date
dicName = 'stats_dic'
outName = 'stats.json'

open(dicName,'w').close()
open(outName,'w').close()

analyze_replays(beginPage=1,endPage=800,dicFileName=dicName,outFileName=outName,start_date=start_date)

print "Finished calculating starting from day: " + start_date
