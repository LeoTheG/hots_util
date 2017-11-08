from time import sleep
import json
import os
import requests
from datetime import date
from dateutil.relativedelta import relativedelta
from heroCounters import analyze_replays

# GOAL: Database updates every week
# Database is current with 1 month of data starting 1 month and 1 week ago
# Every week, grab new data (1 week long starting 2 weeks ago)
# Every week, delete old data (1 week long starting 1 month and 2 weeks ago)

def init_hero_dict(heroDict,hero_name):
    heroDict[hero_name] = {}
    heroDict[hero_name]['total_wins'] = 0
    heroDict[hero_name]['total_losses'] = 0
    heroDict[hero_name]['allies'] = {}
    heroDict[hero_name]['enemies'] = {}
    heroDict[hero_name]['maps'] = {}

# grab old data

start_date= (date.today() + relativedelta(months=-1,weeks=-2)).strftime('%Y-%m-%d')
end_date= (date.today() + relativedelta(months=-1,weeks=-1)).strftime('%Y-%m-%d')
print "grabbing old data from from: " + start_date

oldDicName = 'dic_old_data_'+start_date
oldOutName = 'stats_old_data_'+start_date+'.json'

# create/empty the dic and outfile files
open(oldDicName,'w').close()
open(oldOutName,'w').close()

# arbitrarily large endPage
analyze_replays(beginPage=1,endPage=200,dicFileName=oldDicName,outFileName=oldOutName,start_date=start_date,end_date=end_date)

# grab new data

new_start_date = (date.today() + relativedelta(weeks=-2)).strftime('%Y-%m-%d')
new_end_date = (date.today() + relativedelta(weeks=-1)).strftime('%Y-%m-%d')
newDicName = 'dic_new_data_'+new_start_date
newOutName = 'stats_new_data_'+new_start_date+'.json'
open(newDicName,'w').close()
open(newOutName,'w').close()

analyze_replays(beginPage=1,endPage=200,dicFileName=newDicName,outFileName=newOutName,start_date=new_start_date,end_date=new_end_date)

oldHeroDict={}
currHeroDict={}
newHeroDict={}
currDicName = 'stats_dic'

# delete old data
with open(oldDicName) as ohd, open(currDicName) as chd:
    oldHeroDict = json.load(ohd)
    currHeroDict= json.load(chd)
    for hero in oldHeroDict:
        if hero=='maps':
            for _map in oldHeroDict['maps']:
                for map_hero in oldHeroDict['maps'][_map]:
                    currHeroDict['maps'][_map][map_hero]['wins'] -= oldHeroDict['maps'][_map][map_hero]['wins']
                    currHeroDict['maps'][_map][map_hero]['losses'] -= oldHeroDict['maps'][_map][map_hero]['losses']

        if hero=='talents':
            for talent in oldHeroDict[hero]['talents']:
                for talent_hero in oldHeroDict['talents'][talent]['heroes']:
                    currHeroDict['talents'][talent]['heroes'][talent_hero]['wins'] -= oldHeroDict['talents'][talent]['heroes'][talent_hero]['wins']
                    currHeroDict['talents'][talent]['heroes'][talent_hero]['losses'] -= oldHeroDict['talents'][talent]['heroes'][talent_hero]['losses']
        if hero=='info':
            continue
        currHeroDict[hero]['total_losses'] -= oldHeroDict[hero]['total_losses']
        currHeroDict[hero]['total_wins'] -= oldHeroDict[hero]['total_wins']
        for _map in oldHeroDict[hero]['maps']:
            currHeroDict[hero]['maps'][_map]['wins'] -= oldHeroDict[hero]['maps'][_map]['wins']
            currHeroDict[hero]['maps'][_map]['losses'] -= oldHeroDict[hero]['maps'][_map]['losses']
            for level in oldHeroDict[hero]['maps'][_map]['talents']:
                for talent in oldHeroDict[hero]['maps'][_map]['talents'][level]:
                    currHeroDict[hero]['maps'][_map]['talents'][level][talent]['wins'] -= oldHeroDict[hero]['maps'][_map]['talents'][level][talent]['wins']
                    currHeroDict[hero]['maps'][_map]['talents'][level][talent]['losses'] -= oldHeroDict[hero]['maps'][_map]['talents'][level][talent]['losses']
        for ally in oldHeroDict[hero]['allies']:
            currHeroDict[hero]['allies'][ally]['wins'] -= oldHeroDict[hero]['allies'][ally]['wins']
            currHeroDict[hero]['allies'][ally]['losses'] -= oldHeroDict[hero]['allies'][ally]['losses']
        for enemy in oldHeroDict[hero]['enemies']:
            currHeroDict[hero]['enemies'][enemy]['wins'] -= oldHeroDict[hero]['enemies'][enemy]['wins']
            currHeroDict[hero]['enemies'][enemy]['losses'] -= oldHeroDict[hero]['enemies'][enemy]['losses']

# update with new data
#TODO check for new heroes & maps & talents
with open(newDicName) as nhd, open(currDicName) as chd:
    newHeroDict = json.load(nhd)
    currHeroDict= json.load(chd)
    for hero in newHeroDict:
        if hero=='maps':
            for _map in newHeroDict['maps']:
                if (_map in currHeroDict['maps']) == False:
                    #init new map
                    currHeroDict['maps'][_map]={}
                for map_hero in newHeroDict['maps'][_map]:
                    if (map_hero in currHeroDict['maps'][_map]) == False:
                        #init new map_hero
                        currHeroDict['maps'][_map][map_hero]['wins']=0
                        currHeroDict['maps'][_map][map_hero]['losses']=0
                    currHeroDict['maps'][_map][map_hero]['wins'] += newHeroDict['maps'][_map][map_hero]['wins']
                    currHeroDict['maps'][_map][map_hero]['losses'] += newHeroDict['maps'][_map][map_hero]['losses']
            continue

        if hero=='talents':
            for talent in newHeroDict['talents']:
                if (talent in currHeroDict['talents']) == False:
                    currHeroDict['talents'][talent] = {}
                    currHeroDict['talents'][talent]['description'] = newHeroDict['talents'][talent]['description']
                    currHeroDict['talents'][talent]['short_name'] = newHeroDict['talents'][talent]['short_name']
                    currHeroDict['talents'][talent]['level'] = newHeroDict['talents'][talent]['level']
                    currHeroDict['talents'][talent]['url'] = newHeroDict['talents'][talent]['url']
                    currHeroDict['talents'][talent]['cooldown'] = newHeroDict['talents'][talent]['cooldown']
                    currHeroDict['talents'][talent]['heroes'] = {}

                for talent_hero in newHeroDict['talents'][talent]['heroes']:
                    if (talent_hero in currHeroDict['talents'][talent]['heroes']) == False:
                        currHeroDict['talents'][talent]['heroes'][talent_hero]['wins'] = 0
                        currHeroDict['talents'][talent]['heroes'][talent_hero]['losses'] = 0
                    currHeroDict['talents'][talent]['heroes'][talent_hero]['wins'] += newHeroDict['talents'][talent]['heroes'][talent_hero]['wins']
                    currHeroDict['talents'][talent]['heroes'][talent_hero]['losses'] += newHeroDict['talents'][talent]['heroes'][talent_hero]['losses']
            continue
        if hero=='info':
            currHeroDict['info']['analysis_start_date'] = new_start_date
            currHeroDict['info']['analysis_next_date'] = new_end_date
            continue

        if (hero in currHeroDict) == False:
            init_hero_dict(currHeroDict,hero)
        currHeroDict[hero]['total_losses'] += newHeroDict[hero]['total_losses']
        currHeroDict[hero]['total_wins'] += newHeroDict[hero]['total_wins']
        for _map in newHeroDict[hero]['maps']:
            # init map
            if (_map in currHeroDict[hero]['maps']) == False:
                currHeroDict[hero]['maps'][_map] = {}
                currHeroDict[hero]['maps'][_map]['wins'] = 0
                currHeroDict[hero]['maps'][_map]['losses'] = 0
                currHeroDict[hero]['maps'][_map]['talents'] = 0
            currHeroDict[hero]['maps'][_map]['wins'] += newHeroDict[hero]['maps'][_map]['wins']
            currHeroDict[hero]['maps'][_map]['losses'] += newHeroDict[hero]['maps'][_map]['losses']
            for level in newHeroDict[hero]['maps'][_map]['talents']:
                if (level in currHeroDict[hero]['maps'][_map]['talents']) == False:
                    currHeroDict[hero]['maps'][_map]['talents'][level] = {}
                for talent in newHeroDict[hero]['maps'][_map]['talents'][level]:
                    if (talent in currHeroDict[hero]['maps'][_map]['talents']) == False:
                        currHeroDict[hero]['maps'][_map]['talents'][level][talent] = {}
                        currHeroDict[hero]['maps'][_map]['talents'][level][talent]['wins'] = 0
                        currHeroDict[hero]['maps'][_map]['talents'][level][talent]['losses'] = 0
                    currHeroDict[hero]['maps'][_map]['talents'][level][talent]['wins'] += newHeroDict[hero]['maps'][_map]['talents'][level][talent]['wins']
                    currHeroDict[hero]['maps'][_map]['talents'][level][talent]['losses'] += newHeroDict[hero]['maps'][_map]['talents'][level][talent]['losses']
        for ally in newHeroDict[hero]['allies']:
            if ( ally in currHeroDict[hero]['allies']) == False:
                currHeroDict[hero]['allies'][ally] = {}
                currHeroDict[hero]['allies'][ally]['wins'] = 0
                currHeroDict[hero]['allies'][ally]['losses'] = 0
            currHeroDict[hero]['allies'][ally]['wins'] += newHeroDict[hero]['allies'][ally]['wins']
            currHeroDict[hero]['allies'][ally]['losses'] += newHeroDict[hero]['allies'][ally]['losses']
        for enemy in newHeroDict[hero]['enemies']:
            if (enemy in currHeroDict[hero]['enemies'] == False):
                currHeroDict[hero]['enemies'][enemy]={}
                currHeroDict[hero]['enemies'][enemy]['wins']=0
                currHeroDict[hero]['enemies'][enemy]['losses']=0
            currHeroDict[hero]['enemies'][enemy]['wins'] += newHeroDict[hero]['enemies'][enemy]['wins']
            currHeroDict[hero]['enemies'][enemy]['losses'] += newHeroDict[hero]['enemies'][enemy]['losses']




with open(currDicName) as d:
    oldHeroDict = json.load(d)

with open(oldDicName) as d:
    oldHeroDict = json.load(d)

