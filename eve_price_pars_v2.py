import csv
import json
import requests
from fake_useragent import UserAgent

data = {"market_name": "jita", "items": [{"name": "Dysprosium"}, {"name": "Neodymium"}, {"name": "Promethium"}, {"name": "Thulium"}, 
{"name": "Platinum"}, {"name": "Chromium"}, {"name": "Caesium"}, {"name": "Hafnium"}, {"name": "Cadmium"}, {"name": "Mercury"}, 
{"name": "Technetium"}, {"name": "Titanium"}, {"name": "Vanadium"}, {"name": "Cobalt"}, {"name": "Tungsten"}, {"name": "Scandium"}, 
{"name": "Silicates"}, {"name": "Evaporite Deposits"}, {"name": "Hydrocarbons"}, {"name": "Atmospheric Gases"}, {"name": "Mexallon"}, 
{"name": "Pyerite"}]
}

jdata = requests.post("https://evepraisal.com/appraisal/structured.json", data=json.dumps(data), headers={'User-Agent': UserAgent().chrome}).text

data = json.loads(jdata)
print(type(data))
all_mats = []
for moon_mat in data["appraisal"]["items"]:
	print(moon_mat["name"], " ", moon_mat["prices"]["sell"]["percentile"])
	cur_mat = [moon_mat["name"], moon_mat["prices"]["sell"]["percentile"]]
	all_mats.append(cur_mat)

with open("zalupa_test.csv", "w", newline='') as csv_file:
	writer = csv.writer(csv_file, delimiter=',')
	writer.writerow(["mat", "price"])
	for line in all_mats:
		writer.writerow(line)
print("File writed!")
