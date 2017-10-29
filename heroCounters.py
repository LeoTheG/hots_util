import json
import os
import requests
from datetime import date
from dateutil.relativedelta import relativedelta
from  pprint import pprint


def analyze_replays(beginPage,endPage,game_type="HeroLeague",dicFileName='dic',outFileName='stats.json'):
    #calculates date 1 month ago
    prev_month = date.today() + relativedelta(months=-1)
    correct_day = prev_month.strftime('%Y-%m-%d')

    # DB structure

# {hero_name: {'total_wins': num_wins, 'total_losses': num_losses, 'maps': {map_name: {'wins': num_wins, 'losses': num_losses, 'talents': {level: {'wins': num_wins, 'losses':num_losses}}}}, 'allies': {ally_name: {'wins': num_wins_with, 'losses': num_losses_with}}, 'enemies': {enemy_name: {'wins': num_wins_against, 'losses': num_losses_against}}}}
    # heroDict initial setup
    heroDict = {}


    for i in range(beginPage,endPage+1):
        # check if dictionary exists
        if os.stat(dicFileName).st_size:
            with open(dicFileName) as d:
                heroDict = json.load(d)
                print "loaded dictionary"
        curr_page = i
        print "On page " + str(curr_page)
        print "Requesting response"
        response = requests.get("http://hotsapi.net/api/v1/replays/paged?page="+str(curr_page)+"&game_type="+game_type)
        print "Finished request"

        try:
            data = json.loads(response.text)
        except ValueError:
            # keep track of unprocessed pages
            print "Could not decode page: " + str(curr_page)
            pages = []
            with open("unprocessed_pages.txt","r") as f:
                pages = f.readlines()
            with open("unprocessed_pages.txt","w") as f:
                f.write("".join(pages)+str(curr_page)+"\n")
            continue

        lenReplays = len(data['replays'])

        # decode replays on the page
        for x in range(0,lenReplays):
            currID =  data['replays'.decode('utf-8')][x]['id']

            print "\tRequesting replay id:" + str(currID)
            response = requests.get('http://hotsapi.net/api/v1/replays/'+str(currID))
            print "\tFinished replay request"

            # loads data of certain replay ( got through ID )
            try:
                replayData = json.loads(response.text)
            except ValueError:
                print 'Could not decode replay'
                continue
            arrLen = len(replayData['players'])

            numWinners = 0
            numLosers = 0
            winners = [''] * 5
            losers = [''] * 5
            map_name = replayData['game_map']

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

                    # ##### HERO DB STRUCTURE #####

                    # {hero_name: {'total_wins': num_wins, 'total_losses': num_losses, 'maps': {map_name: {'wins': num_wins, 'losses': num_losses, 'talents': {level: {'wins': num_wins, 'losses':num_losses}}}}, 'allies': {ally_name: {'wins': num_wins_with, 'losses': num_losses_with}}, 'enemies': {enemy_name: {'wins': num_wins_against, 'losses': num_losses_against}}}}

                    # check & add winner key to dict
                    if (winner in heroDict) == False:
                        #heroDict[winner] = dict( [( 'allies', dict( [('wins',0),('losses',0)] ) ), ('ally', dict( [('wins',0),('losses',0)] )) ] )
                        heroDict[winner]['total_wins'] = 0
                        heroDict[winner]['total_losses'] = 0
                        heroDict[winner]['allies'] = {}
                        heroDict[winner]['enemies'] = {}
                        heroDict[winner]['maps'] = {}
                    # check & add maps key to dict[winner]
                    if map_name in heroDict[winner]['maps'] == False:
                        heroDict[winner]['maps'][map_name] = {}
                        heroDict[winner]['maps'][map_name]['wins'] = 0
                        heroDict[winner]['maps'][map_name]['losses'] = 0
                        heroDict[winner]['maps'][map_name]['talents'] = {}
                        heroDict[winner]['maps'][map_name]['talents'] = {}

                       # add loser key & value to heroDict[winner] if nonexistent
                    if (loser in heroDict[winner]['enemy']) == False:
                        heroDict[winner][ = dict( [( 'enemy', dict( [('wins',0),('losses',0)] ) ), ('ally', dict( [('wins',0),('losses',0)] )) ] )
                        #heroDict[winner][loser] = dict([('wins',0),('losses',0)])

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
        with open(dicFileName, 'w') as outfile:
            json.dump(heroDict, outfile)
            print "saved page: " + str(curr_page)
            read_from_dic = True

    with open(outFileName, 'w') as outfile:
        json.dump(heroDict, outfile)

analyze_replays(beginPage=211, endPage=298)
