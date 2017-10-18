import json
import requests
from datetime import date
from dateutil.relativedelta import relativedelta
from  pprint import pprint

#calculates date 1 month ago
prev_month = date.today() + relativedelta(months=-1)
correct_day = prev_month.strftime('%Y-%m-%d')
game_type = "HeroLeague"

heroDict = {}
numPages = 2
for i in range(0,numPages):
    curr_page = i+1
    print "On page " + str(curr_page)
    print "Requesting response"
    #response = requests.get("http://hotsapi.net/api/v1/replays/paged?page="+str(curr_page)+"&start_date="+correct_day+"&game_type="+game_type)
    response = requests.get("http://hotsapi.net/api/v1/replays/paged?page="+str(curr_page)+"&game_type="+game_type)
    print "Finished request"

    data = json.loads(response.text)


    lenReplays = len(data['replays'])

    for x in range(0,lenReplays):
        currID =  data['replays'.decode('utf-8')][x]['id']

        # want to count hero popularity
        response = requests.get('http://hotsapi.net/api/v1/replays/'+str(currID))

        # loads data of certain replay ( got through ID )
        replayData = json.loads(response.text)

        arrLen = len(replayData['players'])

        numWinners = 0
        numLosers = 0
        winners = [''] * 5
        losers = [''] * 5

        # iterate through heroes played in certain match, keeping count
        for i in range (0,arrLen):
            heroName = (replayData['players'][i]['hero']).encode("utf-8")

            # sort winners & losers into 2 arrays
            if replayData['players'][i]['winner'] == True:
                winners[numWinners] = (replayData['players'][i]['hero']).encode("utf-8")
                numWinners += 1
            else:
                losers[numLosers] = (replayData['players'][i]['hero']).encode("utf-8")
                numLosers += 1

        # adds wins and losses to heroDict
        for win in range (0, 5):
            winner = winners[win]
            for lose in range (0,5):
                loser = losers[lose]

                # structure: heroDict[Hero] = dict( loser, dict(wins,losses) )

                # add winner key & value to heroDict if nonexistent
                #print "key: " + winner + ", value: " + str(heroDict[winner])
                if (winner in heroDict) == False:
                    print "Adding winner key: " + winner
                    heroDict[winner] = dict( [( loser, dict( [('wins',0),('losses',0)] ))] )
                # add loser key & value to heroDict[winner] if nonexistent
                if (loser in heroDict[winner]) == False:
                    heroDict[winner][loser] = dict([('wins',0),('losses',0)])

                # increment win
                heroDict[winner][loser]['wins'] += 1

                if (loser in heroDict) == False:
                    heroDict[loser] = dict([(winner,dict([('wins',0),('losses',0)]))])
                # add winner key & value to heroDict[loser] if nonexistent
                if (winner in heroDict[loser]) == False:
                    heroDict[loser][winner] = dict([('wins',0),('losses',0)])

                # increment loss
                heroDict[loser][winner]['losses'] += 1


lenDict = len(heroDict)

with open('stats.txt', 'w') as outfile:
    json.dump(heroDict, outfile)
