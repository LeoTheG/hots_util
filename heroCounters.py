import json
import os
import requests
from datetime import date
from dateutil.relativedelta import relativedelta
from  pprint import pprint

#calculates date 1 month ago
prev_month = date.today() + relativedelta(months=-1)
correct_day = prev_month.strftime('%Y-%m-%d')
game_type = "HeroLeague"

heroDict = {}
beginPage = 161
endPage = 200
dicFileName = 'dic'

for i in range(beginPage,endPage):
    if os.stat(dicFileName).st_size:
        with open(dicFileName) as d:
            heroDict = json.load(d)
            print "loaded dic"
    curr_page = i
    print "On page " + str(curr_page)
    print "Requesting response"
    #response = requests.get("http://hotsapi.net/api/v1/replays/paged?page="+str(curr_page)+"&start_date="+correct_day+"&game_type="+game_type)
    response = requests.get("http://hotsapi.net/api/v1/replays/paged?page="+str(curr_page)+"&game_type="+game_type)
    print "Finished request"

    data = json.loads(response.text)


    lenReplays = len(data['replays'])

    for x in range(0,lenReplays):
        currID =  data['replays'.decode('utf-8')][x]['id']

        print "\tRequesting replay id:" + str(currID)
        response = requests.get('http://hotsapi.net/api/v1/replays/'+str(currID))
        print "\tFinished replay request"

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

   # save dict every page in case of request timeout
    with open('dic', 'w') as outfile:
        json.dump(heroDict, outfile)
        print "saved page: " + str(curr_page)
        read_from_dic = True

with open('stats.txt', 'w') as outfile:
    json.dump(heroDict, outfile)
