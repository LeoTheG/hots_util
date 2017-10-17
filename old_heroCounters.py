import json
import requests
from datetime import date
from dateutil.relativedelta import relativedelta
from  pprint import pprint

# used for enemy heroes
class Hero:
    wins = 0.0
    losses = 0.0
    name = ''
    def __init__(self,name):
        self.name = name
        self.wins = 0.0
        self.losses = 0.0
    def incWin(self):
        self.wins += 1
    def incLoss(self):
        self.losses += 1
    def getTotal(self):
        return self.wins+self.losses
    def getWinPerc(self):
        return self.wins/self.getTotal()
    def getLossPerc(self):
        return self.losses/self.getTotal()
    def getName(self):
        return self.name
    def getWins(self):
        return int(self.wins)
    def getLosses(self):
        return int(self.losses)
class WinLoss:
    enemyHeroes = {}
    heroName = ''
    # creates new Hero object and adds to list
    def __init__(self, name):
        self.enemyHeroes = {}
        self.heroName = name
    def addHero(self, name):
        self.enemyHeroes[name] = Hero(name)
    def incWin(self,heroName):
        if self.enemyHeroes == False:
            self.addHero(heroName)
        if (heroName in self.enemyHeroes) == False:
            self.addHero(heroName)
        self.enemyHeroes[heroName].incWin()
    def incLoss(self,heroName):
        if self.enemyHeroes == False:
            self.addHero(heroName)
        if (heroName in self.enemyHeroes) == False:
            self.addHero(heroName)
        self.enemyHeroes[heroName].incLoss()
    def getWinPerc(self,heroName):
        if self.enemyHeroes == False:
            self.addHero(heroName)
        if (heroName in self.enemyHeroes) == False:
            self.addHero(heroName)
        self.enemyHeroes[heroName].getWinPerc()
    def getHeroes(self):
        return self.enemyHeroes
    def getHero(self,name):
        return self.enemyHeroes[name]

#calculates date 1 month ago
prev_month = date.today() + relativedelta(months=-1)
correct_day = prev_month.strftime('%Y-%m-%d')
game_type = "HeroLeague"

heroDict = {}
for i in range(0,1):
    curr_page = i+1
    print "On page " + str(curr_page)
    print "Requesting response"
    #response = requests.get("http://hotsapi.net/api/v1/replays/paged?page="+str(curr_page)+"&start_date="+correct_day+"&game_type="+game_type)
    response = requests.get("http://hotsapi.net/api/v1/replays/paged?page="+str(curr_page)+"&game_type="+game_type)
    print "Finished request"

    data = json.loads(response.text)


    lenReplays = len(data['replays'])

    for x in range(0,10):
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

                if (winner in heroDict) == False:
                    heroDict[winner] = WinLoss(winner)

                heroDict[winner].incWin(loser)

                if (loser in heroDict) == False:
                    heroDict[loser] = WinLoss(loser)

                heroDict[loser].incLoss(winner)

lenDict = len(heroDict)

'''
file = open("stats.txt","w")

for hero in heroDict:
    enemyHeroes = heroDict[hero].getHeroes()
    for enemyHero in enemyHeroes:
        perclen = len(str(round(enemyHeroes[enemyHero].getWinPerc()*100,3)))
        file.write(hero + " " * (18-len(hero)) +
                str(round(enemyHeroes[enemyHero].getWinPerc()*100,3)) +
                " " * (8-perclen) + enemyHeroes[enemyHero].getName() +
                " " * (18-len(enemyHeroes[enemyHero].getName())) +
                " " * 5 + str(int(enemyHeroes[enemyHero].getTotal())) +
                " " * 5 + str(int(enemyHeroes[enemyHero].getWins())) +
                " " * 5 + str(int(enemyHeroes[enemyHero].getLosses())) + "\n")

file.close()
'''
with open('stats.txt', 'w') as outfile:
    json.dump(heroDict, outfile)
