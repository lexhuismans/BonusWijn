import json
import re

import requests
from bs4 import BeautifulSoup

JSONHEADERS = {
    "Accept": "application/json",
    "Content-Type": "application/json",
    "Accept-Language": "en-us",
    "Host": "www.vivino.com",
    "User-Agent": "android/6.29.3 Model/phone Android/7.0-API24",
    "Accept-Encoding": "gzip, deflate, br",
    "Connection": "keep-alive",
    "X-Requested-With": "XMLHttpRequest",
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
    url_find = "https://www.vivino.com/api/checkout_prices?"
    req_wine = requests.get(url_find, headers=JSONHEADERS, params=PARAMS)

    return req_wine.json()


def get_json_from_query(query):
    temp = query.replace(" ", "+")
    link = u"https://www.vivino.com/search/wines?q=" + temp
    return get_wine_of_url(link)


def add_vivino_data(file):
    with open(file, "r") as read_file:
        data = json.load(read_file)

    combined_data = []
    for wine in data:
        title = wine['title']

        vivino_data = get_json_from_query(title)

        # Get rating and number of review
        wine['rating'] = vivino_data[0]['aggregateRating']['ratingValue']
        wine['numberOfReviews'] = vivino_data[0]['aggregateRating']['reviewCount']
        combined_data.append(wine)

    with open('./processed_data/jumbo_vivino_wines.json', 'w') as fout:
        json.dump(combined_data, fout)


if __name__ == "__main__":
    add_vivino_data("./data/jumbo_filtered_wines.json")
