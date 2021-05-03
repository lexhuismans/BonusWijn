import json

with open("./BonusWijn/backend/processed_data/ah_vivino_wines.json", "r") as read_file:
    data = json.load(read_file)


for wine in data:
    wine['rating'] = float(wine['rating'].replace(",", "."))


data = sorted(data, key=lambda wine: -wine['rating']) 

with open('./BonusWijn/backend/processed_data/sorted_wines.json', 'w') as fout:
    json.dump(data , fout)