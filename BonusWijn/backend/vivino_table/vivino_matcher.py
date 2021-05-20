import json
import time

from pprint import pprint

from vivino import get_json_from_query


def find_title(title):
    with open('./vivino_data/vivino_data.json', 'r') as file:
        vivino_data = json.load(file)
        if title in vivino_data:
            return vivino_data[title]
        else:
            vivino_json = get_json_from_query(title)
            vivino_data.append({title: vivino_json})
            pprint(vivino_data)
            with open('./vivino_data/vivino_data.json', 'w') as file:
                json.dump(vivino_data, file)
            return vivino_json

# Reformat
with open('./vivino_data/vivino_data.json', 'r') as file:
    vivino_data = json.load(file)
    new_vivino_list = []
    for item in vivino_data:
        title = list(item.keys())[0]
        viv_json = item[title]
        new_vivino_list.append({'title': title, 'vivino': viv_json})

    with open('./vivino_data/vivino_data_new.json', 'w') as outfile:
        json.dump(new_vivino_list, outfile)

'''
with open('./raw_supermarket/jumbo_wines_titles.json', 'r') as file:
    title_list = json.load(file)
    for title in title_list:
        vivino = find_title(title)
        pprint(vivino)
        time.sleep(10)
'''