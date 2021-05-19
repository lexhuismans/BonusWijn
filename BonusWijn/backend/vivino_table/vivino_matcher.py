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

with open('./raw_supermarket/jumbo_wines_titles.json', 'r') as file:
    title_list = json.load(file)
    for title in title_list:
        vivino = find_title(title)
        pprint(vivino)
        time.sleep(10)
