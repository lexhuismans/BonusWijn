import json
import pickle



with open('./ah_name_data/ah_wines.json', 'r') as outfile:
    data = json.load(outfile)

wine_names = []
count = 0
for wine in data:
    wine_names.append(wine['title'])
    print(wine['title'])

# with open('./ah_name_data/ah_wine_names.json', 'w') as outfile:
#     json.dump(wine_names, outfile)
