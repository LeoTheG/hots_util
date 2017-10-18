import json
import requests

response = requests.get("http://hotsapi.net/api/v1/heroes")
data = json.loads(response.text)
numHeroes = len(data)
heroNames = []

for count in range(0,numHeroes):
    heroNames.extend([str(data[count]['short_name'])])

with open("hero_names.txt", "w") as output:
    for name in heroNames:
        output.write(name+"\n")
    #output.write(str(heroNames))
