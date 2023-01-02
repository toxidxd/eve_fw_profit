import csv
import json
import requests
from fake_useragent import UserAgent

data = {"market_name": "amarr",
        "items": [{"name": "Tritanium"},
                  {"name": "Pyerite"},
                  {"name": "Mexallon"},
                  {"name": "Isogen"},
                  {"name": "Nocxium"},
                  {"name": "Zydrine"},
                  {"name": "Megacyte"},
                  {"name": "Auto-Integrity Preservation Seal"},
                  {"name": "Life Support Backup Unit"},
                  {"name": "Coercer Navy Issue"},
                  {"name": "Omen Navy Issue"},
                  {"name": "Augoror Navy Issue"},
                  {"name": "Prophecy Navy Issue"}]
        }

jdata = requests.post("https://evepraisal.com/appraisal/structured.json",
                      data=json.dumps(data),
                      headers={'User-Agent': UserAgent().chrome}).text

data = json.loads(jdata)
print(type(data))
all_mats = []

for material in data["appraisal"]["items"]:
    print(material["name"], " sell", material["prices"]["sell"]["percentile"])
    print(material["name"], " buy", material["prices"]["buy"]["percentile"])

    cur_mat = [material["name"],
               str(material["prices"]["sell"]["percentile"]).replace('.', ','),
               str(material["prices"]["buy"]["percentile"]).replace('.', ',')]

    all_mats.append(cur_mat)

with open("materials_price.csv", "w", newline='') as csv_file:
    writer = csv.writer(csv_file, delimiter=',')
    writer.writerow(["mat", "sell", "buy"])
    for line in all_mats:
        writer.writerow(line)

print("File wrote!")
