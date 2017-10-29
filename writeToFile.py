file = open("testfile.txt","w")
hero = "wow"
hero2 = "lollolol"
x = 9
perc = 99.999192319239123912931
otherHero = "cool"
numGames = 75
file.write(hero + " " * (17-len(hero)) + str(round(perc,3)) +
        " " * 5 + otherHero + " " * (17-len(otherHero)) +
        " " * 5 + str(numGames) + "\n")
#file.write(otherHero + " " * (15-len(otherHero)) + str(round(perc,3)) +
#        " percent win rate vs " + otherHero + "\n")
file.close()
