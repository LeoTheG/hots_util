import json
import requests
from datetime import date
from dateutil.relativedelta import relativedelta

#calculates date 1 month ago
curr_page = 1
prev_month = date.today() + relativedelta(months=-1)
correct_day = prev_month.strftime('%Y-%m-%d')

response = requests.get("http://hotsapi.net/api/v1/replays/paged?page="+str(curr_page)+"&start_date="+correct_day)

#rj = response.json()
data = json.loads(response.text)

print data['replays'][0]['id']

#want to find most popular heroes

