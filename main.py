import json
import requests
from datetime import date
from dateutil.relativedelta import relativedelta
from  pprint import pprint

#calculates date 1 month ago
curr_page = 1
prev_month = date.today() + relativedelta(months=-1)
correct_day = prev_month.strftime('%Y-%m-%d')

response = requests.get("http://hotsapi.net/api/v1/replays/paged?page="+str(curr_page)+"&start_date="+correct_day)

#rj = response.json()
#pprint(rj)
data = json.loads(response.text)

heroDict = {}

lenReplays = len(data['replays'])
print "type of data is: " + str(data.__class__)
print "lenReplays = "+ str(lenReplays)

lenReplays = 10
# loop over all replays
for x in range(0,lenReplays):

    print "Running loop iteration: " + str(x)

    currID =  data['replays'.decode('utf-8')][x]['id']

    print("got id: "+str(currID))

    # want to count hero popularity
    # loads data of certain replay ( got through ID )
    response = requests.get('http://hotsapi.net/api/v1/replays/'+str(currID))
    replayData = json.loads(response.text)

    arrLen = len(replayData['players'])

    # iterate through heroes played in certain match, keeping count
    for i in range (0,arrLen):
        heroName = (replayData['players'][i]['hero']).encode("utf-8")
        if heroName in heroDict:
            heroDict[heroName] += 1
        else:
            heroDict[heroName] = 1

lenDict = len(heroDict)

for key in heroDict:
    print "key: %s, value: %s" % (key, heroDict[key])


