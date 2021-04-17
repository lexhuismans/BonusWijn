import json
import re

import requests
from bs4 import BeautifulSoup

"""
# URL om wijn te zoeken, je moet minimaal een filter geven (met params)
url = 'https://www.vivino.com/api/explore/explore?country_code=NL&currency_code=EUR&grape_filter=varietal&min_rating=3.5&order_by=ratings_average&order=desc&page=1&price_range_max=30&price_range_min=7&wine_type_ids[]=1&wine_type_ids[]=2'

# Had ergens gelezen dat je hier token kan krijgen oauth is een ding om acces te managen.
url2 = 'http://api.vivino.com/oauth/token' # For getting token

# URL om wijn te zoeken
url3 = 'https://www.vivino.com/api/explore/explore?country_code=NL&currency_code=EUR'

# URL To search wine
url4 = 'https://www.vivino.com/search/wines?q=rioja+campo+viejo'

# Some random URLs
url5 = 'https://www.vivino.com/api/signals'
"""


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


def get_wine_from_URL(url):
    """
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


def get_wine_from_ID(url):
    """
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

    # Search with ID
    id = re.findall("(?<=data-vintage=')\d+", req.text)

    PARAMS = {"vintage_id": int(id[0])}

    url_find = "https://www.vivino.com/api/checkout_prices?"
    req_wine = requests.get(url_find, headers=JSONHEADERS, params=PARAMS)

    return req_wine.json()
