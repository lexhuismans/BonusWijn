import json
import time
import pickle

from pprint import pprint

from vivino import get_json_from_query


def find_title(title, wine_name_dict):
        print(title)
        if title in wine_name_dict:
            print("already contained")
            return wine_name_dict[title]
        else:
            print('wine not contained yet')
            try:
                vivino_json = get_json_from_query(title)
            except:
                vivino_json = "no data"
            wine_name_dict[title] = vivino_json
            time.sleep(5)
            return vivino_json


# with open('./raw_supermarket/jumbo_wines_titles.json', 'r') as file:
#     title_list = json.load(file)

with open('./raw_supermarket/ah_wine_names.json', 'r') as file:
    title_list = json.load(file)


with open('./raw_supermarket/jumbo_wines_titles.json', 'r') as file:
    title_list2 = json.load(file)

title_list = title_list + title_list2

with open('./vivino_data/name_data_dict_copy.pickle', 'rb') as handle:
    wine_name_dict = pickle.load(handle)

for index, title in enumerate(title_list):
    vivino = find_title(title, wine_name_dict)
    if (index % 100) == 0:
        pprint(vivino)
        with open('./vivino_data/name_data_dict_complete.pickle', 'wb') as handle:
            pickle.dump(wine_name_dict, handle)
