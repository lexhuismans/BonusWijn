import json
import pprint
import time
import re

import requests

JSONHEADERS = {
    "Accept": "application/json",
    "Content-Type": "application/json",
    "Accept-Language": "en-us",
    "Host": "www.vivino.com",
    "User-Agent": "android/6.29.3 Model/phone Android/7.0-API24",
    #"Accept-Encoding": "gzip, deflate, br",
    #"Connection": "keep-alive",
    #"X-Requested-With": "XMLHttpRequest",
}

HEADERS = {
    "Accept-Language": "en-us",
    "Host": "www.vivino.com",
    "User-Agent": "android/6.29.3 Model/phone Android/7.0-API24",
    "Accept-Encoding": "gzip, deflate, br",
    "Connection": "keep-alive",
    "Type-Name": "uwp_wine_lookup",
    "X-Requested-With": "XMLHttpRequest",
}

def get_first_wine_url(url):
    """
    Werkt volgensmij nog niet helemaal lekker.
    Params
    ------
    url : str
        url with search query.

    Returns
    -------
    req_wine : json
        json of first wine in search query.
    """
    req = requests.get(url, headers=HEADERS)

    # Search for ID
    id = re.findall("(?<=data-vintage=')\d+", req.text)

    # Add ID of first wine in query
    PARAMS = {"vintage_id": int(id[0])}

    # Get json from ID
    #url_find = "https://www.vivino.com/api/checkout_prices?"
    #req_wine = requests.get(url_find, headers=JSONHEADERS, params=PARAMS)
    url_find = "https://www.vivino.com/api/vintages/" + id[0]
    req_wine = requests.get(url_find, headers=JSONHEADERS)
    return req_wine.json()


def get_json_from_query(query):
    temp = query.replace(" ", "+")
    link = u"https://www.vivino.com/search/wines?q=" + temp
    return get_first_wine_url(link)


def find_title(title, wine_name_dict):
    '''
    Find vivino wine json in database. 
    '''
    if title in wine_name_dict:
        print("already contained")
        return filter_vivino_data(wine_name_dict[title])
    else:
        print('Wine not contained yet: ', title)
        try:
            vivino_json = get_json_from_query(title)
        except:
            vivino_json = None
        wine_name_dict[title] = vivino_json
        # !!Ook nog toevoegen aan database!!!
        return filter_vivino_data(vivino_json)


def filter_vivino_data(vivino_data):
    '''
    Add formatted vivino data to json. 
    '''
    if vivino_data is None:
        return None

    filtered_vivino = {}

    # Get rating and number of review
    wine_data = vivino_data['vintage']['wine']
    if int(wine_data['vintages'][0]['statistics']['ratings_count']) > 1000:
        filtered_vivino['rating'] = wine_data['vintages'][1]['statistics']['ratings_average']
        filtered_vivino['numberOfReviews'] = wine_data['vintages'][1]['statistics']['ratings_count']
    else:  # Take all year ratings 
        filtered_vivino['rating'] = vivino_data['vintage']['statistics']['ratings_average']
        filtered_vivino['numberOfReviews'] = vivino_data['vintage']['statistics']['ratings_count']

    # Grape
    try:
        filtered_vivino['grape'] = wine_data['grapes'][0]['name']
        filtered_vivino['grape_count'] = wine_data['grapes'][0]['wines_count']
    except IndexError:
        filtered_vivino['grape'] = 'Other'
        filtered_vivino['grape_count'] = 0

    # Type
    type = wine_data['type_id']
    if type == 1:
        filtered_vivino['type'] = 'Red'
    elif type == 2:
        filtered_vivino['type'] = 'White'
    elif type == 3:
        filtered_vivino['type'] = 'Bubbles'
    elif type == 4:
        filtered_vivino['type'] = 'Ros\u00e9'
    else:
        filtered_vivino['type'] = 'Other'

    # Region
    try:
        filtered_vivino['country'] = wine_data['region']['country']['name']
        filtered_vivino['region'] = wine_data['region']['name']
    except TypeError:
        filtered_vivino['country'] = 'Other'
        filtered_vivino['region'] = 'Other'

    # Food
    foods = []
    for food in wine_data['foods']:
        if 'fish' in food['name']:
            foods.append('Fish')
        else:
            foods.append(food['name'])
    filtered_vivino['foods'] = foods
        
    return filtered_vivino