import json



with open('./vivino_data/vivino_data.json', 'r') as file:
    vivino_data = json.load(file)


print(len(vivino_data))

for wine in vivino_data:
    print(wine)