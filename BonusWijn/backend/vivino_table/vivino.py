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

'''
# Old
def get_wine_of_url(url):
    """
    Get the first wine in search url
    Params
    ------
    url : str
        url with search query.

    Returns
    -------
    req_wine : json
        json containing first few wines of search query.
    """
    req = requests.get(url, headers=HEADERS)

    # Search in html
    soup = BeautifulSoup(req.text, "html.parser")
    # Find string that converts to json (First <script type='application/ld+json'> )
    jsonstr = str(soup.find("script", attrs={"type": "application/ld+json"}))
    j = jsonstr[35:-9]

    return json.loads(j)
'''

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


def add_vivino_data(file = "./data/jumbo_filtered_wines.json"):
    with open(file, "r") as read_file:
        data = json.load(read_file)

    combined_data = []
    for wine in data:
        title = wine['title']

        vivino_data = get_json_from_query(title)

        # Get rating and number of review
        wine_data = vivino_data['vintage']['wine']
        wine['rating'] = wine_data['vintages'][1]['statistics']['ratings_average']
        wine['numberOfReviews'] = wine_data['vintages'][1]['statistics']['ratings_count']
        #wine['title'] = vivino_data['name']  # Change to vivino title
        print(wine['title'])

        # Grape
        try:
            wine['grape'] = wine_data['grapes'][0]['name']
            wine['grape_count'] = wine_data['grapes'][0]['wines_count']
        except IndexError:
            wine['grape'] = 'Other'
            wine['grape_count'] = 0

        # Type
        type = wine_data['type_id']
        if type == 1:
            wine['type'] = 'Red'
        elif type == 2:
            wine['type'] = 'White'
        elif type == 3:
            wine['type'] = 'Bubbles'
        elif type == 4:
            wine['type'] = 'Ros\u00e9'
        else:
            wine['type'] = 'Other'

        # Region
        try:
            wine['country'] = wine_data['region']['country']['name']
            wine['region'] = wine_data['region']['name']
        except TypeError:
            wine['country'] = 'Other'
            wine['region'] = 'Other'
        combined_data.append(wine)

        time.sleep(3)

    with open(file, 'w') as fout:
        json.dump(combined_data, fout)

    return combined_data

if __name__ == "__main__":
    #data = get_first_wine_url("https://www.vivino.com/search/wines?q=Viñas+del+Vero+Luces+blanco")
    add_vivino_data("./processed_data/sorted_wines.json")
    #print(pprint.pprint(data))
