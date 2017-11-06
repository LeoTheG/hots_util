# -*- coding: utf-8 -*-
from time import sleep
import json
import os
import requests
from datetime import date
from dateutil.relativedelta import relativedelta

# DB structure
# {'talents': {talent_name: {'heroes': {heroName: {'wins','losses'}},'short_name', 'description','url','cooldown','level'}},'maps': { map_name: { hero_name: { 'wins', 'losses'} } }, hero_name: {'total_wins', 'total_losses', 'maps': {map_name: {'wins', 'losses', 'talents': {level: {talent_name: {'wins', 'losses'}}}}}, 'allies': {ally_name: {'wins': num_wins_with, 'losses': num_losses_with}}, 'enemies': {enemy_name: {'wins': num_wins_against, 'losses': num_losses_against}}}}

LEVELS = ['1','4','7','10','13','16','20']

def check_and_init_talent_names(heroDict,hero_name,map_name,talent_dict):
    heroDict['talents'] = {}
    if talent_dict == None:
        print "No talent dict"
        return
    i = 0
    while i < len(talent_dict):
        curr_level = LEVELS[i]
        talent_name = talent_dict[curr_level]

        # create heroDict['talents'] dicts
        if (talent_name in heroDict['talents']) == False:
            response = requests.get("http://hotsapi.net/api/v1/talents/"+talent_name)
            data = json.loads(response.text)
            heroDict['talents'][talent_name] = {}
            heroDict['talents'][talent_name]['heroes'] = {}
            heroDict['talents'][talent_name]['short_name'] = data['title']
            heroDict['talents'][talent_name]['description'] = data['description']
            heroDict['talents'][talent_name]['url'] = data['icon_url']['64x64']
            heroDict['talents'][talent_name]['cooldown'] = data['cooldown']
            heroDict['talents'][talent_name]['level'] = data['level']
            print "Creating heroDict['talents'] short name:"+heroDict['talents'][talent_name]['short_name']
        for hero in data['heroes']:
            if hero[-3:] == 'cio':
                hero = 'Lucio'

            if (hero in heroDict['talents'][talent_name]['heroes']) == False:
                heroDict['talents'][talent_name]['heroes'][hero] = {}
                heroDict['talents'][talent_name]['heroes'][hero]['wins'] = 0
                heroDict['talents'][talent_name]['heroes'][hero]['losses'] = 0


        short_talent_name = heroDict['talents'][talent_name]['short_name']
        # create heroDict[hero_name]['maps'][map_name]['talents']
        if (short_talent_name in heroDict[hero_name]['maps'][map_name]['talents'][curr_level]) == False:
            heroDict[hero_name]['maps'][map_name]['talents'][curr_level][short_talent_name] = {}
            heroDict[hero_name]['maps'][map_name]['talents'][curr_level][short_talent_name]['wins'] = 0
            heroDict[hero_name]['maps'][map_name]['talents'][curr_level][short_talent_name]['losses'] = 0
        i += 1

def init_map_dict(heroDict,map_name,hero_name):
    heroDict['maps'][map_name][hero_name] = {}
    heroDict['maps'][map_name][hero_name]['wins'] = 0
    heroDict['maps'][map_name][hero_name]['losses'] = 0
def init_enemy_in_enemies(heroDict,hero_name, enemy_name):
    heroDict[hero_name]['enemies'][enemy_name] = {}
    heroDict[hero_name]['enemies'][enemy_name]['wins'] = 0
    heroDict[hero_name]['enemies'][enemy_name]['losses'] = 0

def init_hero_dict(heroDict,hero_name):
    heroDict[hero_name] = {}
    heroDict[hero_name]['total_wins'] = 0
    heroDict[hero_name]['total_losses'] = 0
    heroDict[hero_name]['allies'] = {}
    heroDict[hero_name]['enemies'] = {}
    heroDict[hero_name]['maps'] = {}

def init_hero_map_dict(heroDict,hero_name, map_name):

    heroDict[hero_name]['maps'][map_name] = {}
    heroDict[hero_name]['maps'][map_name]['wins'] = 0
    heroDict[hero_name]['maps'][map_name]['losses'] = 0
    heroDict[hero_name]['maps'][map_name]['talents'] = {}

    # add levels to talents
    num_levels = len(LEVELS)
    for i in range (0, num_levels):
        curr_level = LEVELS[i]
        heroDict[hero_name]['maps'][map_name]['talents'][curr_level] = {}

prev_month = date.today() + relativedelta(months=-1)
correct_day = prev_month.strftime('%Y-%m-%d')

def analyze_replays(beginPage,endPage,game_type="HeroLeague",dicFileName='dic',outFileName='stats.json',correct_day=correct_day,one_week=False,one_month=True):
    #calculates date 1 month ago
    first_run = True

    heroDict = {}
    heroDict['maps'] = {}

    for i in range(beginPage,endPage+1):
        # check if dictionary exists
        if os.stat(dicFileName).st_size:
            with open(dicFileName) as d:
                heroDict = json.load(d)
                print "loaded dictionary"
        curr_page = i
        if first_run == False:
            print "Sleeping"
            sleep(60)
        first_run = False
        print "On page " + str(curr_page)
        end_date = (date.today() + relativedelta(weeks=-1)).strftime('%Y-%m-%d')
        print "Requesting response from http://hotsapi.net/api/v1/replays/paged?page="+str(curr_page)+"&start_date="+correct_day+"&end_date="+end_date+"&game_type="+game_type
        #response = requests.get("http://hotsapi.net/api/v1/replays/paged?page="+str(curr_page)+"&game_type="+game_type,timeout=60000)
        #TODO: Make one_week/one_month better coded
        response = requests.get("http://hotsapi.net/api/v1/replays/paged?page="+str(curr_page)+"&start_date="+correct_day+"&end_date="+end_date+"&game_type="+game_type,timeout=60000)
        '''
        if one_week:
            new_day = (date.today() + relativedelta(weeks=-1)).strftime('%Y-%m-%d')
            print "from " + "http://hotsapi.net/api/v1/replays/paged?page="+str(curr_page)+"&start_date="+correct_day+"&end_date="+new_day+"&game_type="+game_type
            response = requests.get("http://hotsapi.net/api/v1/replays/paged?page="+str(curr_page)+"&start_date="+correct_day+"&end_date="+new_day+"&game_type="+game_type,timeout=60000)
        elif one_month:
            new_day = (date.today() + relativedelta(weeks=-1)).strftime('%Y-%m-%d')
            response = requests.get("http://hotsapi.net/api/v1/replays/paged?page="+str(curr_page)+"&start_date="+correct_day+"&end_date="+new_day+"&game_type="+game_type,timeout=60000)

        else:
            print "from " + "http://hotsapi.net/api/v1/replays/paged?page="+str(curr_page)+"&start_date="+correct_day+"&game_type="+game_type
            response = requests.get("http://hotsapi.net/api/v1/replays/paged?page="+str(curr_page)+"&start_date="+correct_day+"&game_type="+game_type,timeout=60000)
            '''
        print "Finished request"

        try:
            data = json.loads(response.text)
        except ValueError as e:
            # keep track of unprocessed pages
            print "Could not decode page: " + str(curr_page)
            print e.message
            break
            '''
            pages = []
            with open("unprocessed_pages.txt","r") as f:
                pages = f.readlines()
            with open("unprocessed_pages.txt","w") as f:
                f.write("".join(pages)+str(curr_page)+"\n")
            continue
            '''

        lenReplays = len(data['replays'])

        # decode replays on the page
        for x in range(0,lenReplays):
            # request specific replay
            currID =  data['replays'.decode('utf-8')][x]['id']
            print "\tRequesting replay id:" + str(currID)
            response = requests.get('http://hotsapi.net/api/v1/replays/'+str(currID))
            print "\tFinished replay request"

            # loads data of certain replay ( got through ID )
            try:
                replayData = json.loads(response.text)
            except ValueError as e:
                print 'Could not decode replay'
                print e.message
                continue

            num_players = len(replayData['players'])

            numWinners = 0
            numLosers = 0
            winners = [''] * 5
            losers = [''] * 5
            map_name = replayData['game_map']

            # check & add maps to 'maps' dict
            if (map_name in heroDict['maps']) == False:
                heroDict['maps'][map_name] = {}

            # iterate through heroes played in certain match, keeping count
            for i in range (0, num_players):
                hero_name = (replayData['players'][i]['hero']).encode("utf-8")
                if hero_name[-3:] == 'cio':
                    hero_name = 'Lucio'

                # check & add heroes to specific map
                if ( hero_name in heroDict['maps'][map_name] ) == False:
                    init_map_dict(heroDict,map_name, hero_name)
                # check & add hero keys to dict
                if (hero_name in heroDict) == False:
                    init_hero_dict(heroDict,hero_name)
                # check & add map name
                if (map_name in heroDict[hero_name]['maps']) == False:
                    init_hero_map_dict(heroDict,hero_name, map_name)

                # check & add talent names
                check_and_init_talent_names(heroDict,hero_name,map_name,replayData['players'][i]['talents'])

                # sort winners & losers into 2 arrays
                if replayData['players'][i]['winner'] == True:
                    heroDict['maps'][map_name][hero_name]['wins'] += 1

                    winners[numWinners] = (replayData['players'][i]['hero']).encode("utf-8")
                    if winners[numWinners][-3:] == 'cio':
                        winners[numWinners] = 'Lucio'
                    numWinners += 1
                    heroDict[hero_name]['total_wins'] += 1
                    heroDict[hero_name]['maps'][map_name]['wins'] += 1

                    # increment wins for talents on map
                    if replayData['players'][i]['talents'] == None:
                        continue
                    for lev in range (0, len(replayData['players'][i]['talents'])):
                        curr_level = LEVELS[lev]
                        talent_name = replayData['players'][i]['talents'][curr_level]
                        short_talent_name = heroDict['talents'][talent_name]['short_name']
                        heroDict[hero_name]['maps'][map_name]['talents'][curr_level][short_talent_name]['wins'] += 1
                        if (hero_name in heroDict['talents'][talent_name]) == False:
                            print "Creating talent: " + talent_name
                            heroDict['talents'][talent_name][hero_name] = {}
                            heroDict['talents'][talent_name][hero_name]['wins'] = 0
                            heroDict['talents'][talent_name][hero_name]['losses'] = 0
                        heroDict['talents'][talent_name][hero_name]['wins'] += 1

                else:
                    heroDict['maps'][map_name][hero_name]['losses'] += 1
                    heroDict[hero_name]['maps'][map_name]['losses'] += 1

                    losers[numLosers] = (replayData['players'][i]['hero']).encode("utf-8")
                    if losers[numLosers][-3:] == 'cio':
                        losers[numLosers] = 'Lucio'
                    numLosers += 1
                    heroDict[hero_name]['total_losses'] += 1

                    # increment losses for talents on map
                    #num_levels = len(LEVELS)
                    #for lev in range (0, num_levels):
                    if (replayData['players'][i]['talents']) == None:
                        continue

                    for lev in range (0, len(replayData['players'][i]['talents'])):
                        curr_level = LEVELS[lev]
                        talent_name = replayData['players'][i]['talents'][curr_level]
                        short_talent_name = heroDict['talents'][talent_name]['short_name']
                        heroDict[hero_name]['maps'][map_name]['talents'][curr_level][short_talent_name]['losses'] += 1
                        if (hero_name in heroDict['talents'][talent_name]) == False:
                            print "Creating talent: " + talent_name
                            heroDict['talents'][talent_name][hero_name] = {}
                            heroDict['talents'][talent_name][hero_name]['wins'] = 0
                            heroDict['talents'][talent_name][hero_name]['losses'] = 0
                        heroDict['talents'][talent_name][hero_name]['losses'] += 1

            # add to allies dict of losers
            lose_count = -1
            for lose in range(0, 5):
                lose_count += 1
                loser = losers[lose]
                if loser[-3:] == 'cio':
                    loser = 'Lucio'
                ally_count = 0
                # loop through allies of losers
                while ally_count < 5:
                    ally_name = losers[ally_count]
                    if ally_name[-3:] == 'cio':
                        ally_name = 'Lucio'
                    # do not add self as ally
                    if ally_count != lose_count:
                        # check for ally key
                        if (ally_name in heroDict[loser]['allies']) == False:
                            heroDict[loser]['allies'][ally_name] = {}
                            heroDict[loser]['allies'][ally_name]['wins'] = 0
                            heroDict[loser]['allies'][ally_name]['losses'] = 0

                        heroDict[loser]['allies'][ally_name]['losses'] += 1
                    ally_count += 1

            # adds wins and losses to heroDict
            # also add ally wins to winners
            win_count = -1
            for win in range (0, 5):
                win_count += 1
                winner = winners[win]
                if winner[-3:] == 'cio':
                    winner = 'Lucio'

                # add to allies dict
                ally_count = 0
                while (ally_count < 5):
                    # do not add self as ally
                    ally_name = winners[ally_count]
                    if ally_name[-3:] == 'cio':
                        ally_name = 'Lucio'
                    if ally_count != win_count:
                        # check for ally key
                        if (ally_name in heroDict[winner]['allies']) == False:
                            heroDict[winner]['allies'][ally_name] = {}
                            heroDict[winner]['allies'][ally_name]['wins'] = 0
                            heroDict[winner]['allies'][ally_name]['losses'] = 0

                        heroDict[winner]['allies'][ally_name]['wins'] += 1
                    ally_count += 1

                # increment wins & losses
                for lose in range (0,5):
                    loser = losers[lose]

                    # check & add to enemies
                    if (loser in heroDict[winner]['enemies']) == False:
                        init_enemy_in_enemies(heroDict,winner,loser)
                    if (winner in heroDict[loser]['enemies']) == False:
                        init_enemy_in_enemies(heroDict,loser,winner)

                    # increment win & loss
                    heroDict[winner]['enemies'][loser]['wins'] += 1
                    heroDict[loser]['enemies'][winner]['losses'] += 1

       # save dict every page in case of request timeout
        with open(dicFileName, 'w') as outfile:
            print "Dumping dic to " + dicFileName
            json.dump(heroDict, outfile)
            print "saved page: " + str(curr_page)
            read_from_dic = True

        with open(outFileName, 'w') as outfile:
            json.dump(heroDict, outfile)
