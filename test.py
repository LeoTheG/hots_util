import json
import requests
from datetime import date
from dateutil.relativedelta import relativedelta
from time import sleep
from heroCounters import analyze_replays


prev_month = date.today() + relativedelta(months=-1,weeks=-1)
correct_day = prev_month.strftime('%Y-%m-%d')
print "Calculating starting from day: " + correct_day
dicName = 'test_stats_dic'
outName = 'test_stats.json'
beginPage = 234
endPage = 600

#open(dicName,'w').close()
#open(outName,'w').close()

analyze_replays(beginPage=beginPage,endPage=endPage,dicFileName=dicName,outFileName=outName,correct_day=correct_day)

print "Finished calculating starting from day: " + correct_day
