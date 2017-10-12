import pandas as pd
from pprint import pprint
import requests
from datetime import date
from dateutil.relativedelta import relativedelta

#calculates date 1 month ago
curr_page = 1
prev_month = date.today() + relativedelta(months=-1)
correct_day = prev_month.strftime('%Y-%m-%d')

response = requests.get("http://hotsapi.net/api/v1/replays/paged?page="+str(curr_page)+"&start_date="+correct_day)

rj = response.json()

'''
rlist = list(rj.keys())
print(len(rlist))
print(rlist.pop(1))
'''

pprint(rj)
#df = pd.read_json(response.text, orient='columns')

#print(df[['id']])
#print(df)
