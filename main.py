import json
import requests
from datetime import date
from dateutil.relativedelta import relativedelta
from time import sleep
from heroCounters import analyze_replays


prev_month = date.today() + relativedelta(months=-1)
correct_day = prev_month.strftime('%Y-%m-%d')
print "Analyzing 1 Month of Replays starting from: " + correct_day
dicName = 'stats_dic'
outName = 'stats.json'

open(dicName,'w').close()
open(outName,'w').close()

analyze_replays(beginPage=1,endPage=500,dicFileName=dicName,outFileName=outName,correct_day=correct_day)

print "Finished calculating starting from day: " + correct_day
