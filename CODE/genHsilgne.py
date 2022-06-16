#Generates Hsilgne.json and Hsilgne.txt language files from english.json and english.txt

#Gsilgne is english backwards, and is only to show that localisation actually works

import json

def rev(str):
    return " ".join(map(lambda a:a[::-1],str.split(" ")))

with open("./CODE/translations/english.json") as file:
    translationData = json.load(file)

for item in translationData["translations"].items():
    translationData["translations"][item[0]] = rev(item[1])

translationData["name"] = rev(translationData["name"])

with open("./CODE/translations/hsilgne.json", "w") as file:
    json.dump(translationData, file, indent=4)

about = open("./CODE/about/english.txt").read()
about = rev(about)
open("./CODE/about/hsilgne.txt", "w").write(about)