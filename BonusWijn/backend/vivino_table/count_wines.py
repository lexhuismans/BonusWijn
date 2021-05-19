import json
import pickle



with open('./ah_name_data/ah_wines.json', 'r') as outfile:
    data = json.load(outfile)

print(len(data['products']))

for wine in data['products']:
