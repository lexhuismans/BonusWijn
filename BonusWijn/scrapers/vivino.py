import requests
import json
from bs4 import BeautifulSoup
import re

url = 'https://www.vivino.com/api/explore/explore?country_code=NL&currency_code=EUR&grape_filter=varietal&min_rating=3.5&order_by=ratings_average&order=desc&page=1&price_range_max=30&price_range_min=7&wine_type_ids[]=1&wine_type_ids[]=2'

HEADERS = {
    'Accept': 'application/json',
    'Content-Type': 'application/json',
    'Accept-Language': 'en-us',
    'Host': 'www.vivino.com',
    'User-Agent': 'android/6.29.3 Model/phone Android/7.0-API24',
    'Accept-Encoding': 'gzip, deflate, br',
    'Connection': 'keep-alive',
    'X-Requested-With': 'XMLHttpRequest',
}

payload = {'grant_type': 'client_credentials', 'scope': 'api:read'}

client_id = '<client_id>'
client_secret = '<client_secret>'

url3 = 'https://www.vivino.com/api/explore/explore?country_code=NL&currency_code=EUR'

req = requests.get(url, headers=HEADERS)
#print(req.json())

HEADERS = {
    'Accept-Language': 'en-us',
    'Host': 'www.vivino.com',
    'User-Agent': 'android/6.29.3 Model/phone Android/7.0-API24',
    'Accept-Encoding': 'gzip, deflate, br',
    'Connection': 'keep-alive',
    'Type-Name': 'uwp_wine_lookup',
    'X-Requested-With': 'XMLHttpRequest',
}

url4 = 'https://www.vivino.com/search/wines?q=rioja+campo+viejo'
url5 = 'https://www.vivino.com/api/signals'
req = requests.get(url4, headers=HEADERS)

# Search in html
soup = BeautifulSoup(req.text, "html.parser")
jsonstr = str(soup.find("script", attrs={"type": "application/ld+json"}))
j = jsonstr[35:-9]
print(json.loads(j))



# Search with ID
id = re.findall("(?<=data-vintage=')\d+", req.text)

PARAMS = {
    'vintage_id' : int(id[0])
}

url_find = 'https://www.vivino.com/api/checkout_prices?'
req_wine = requests.get(url_find, headers=HEADERS, params=PARAMS)
print(req_wine.json())

url2 = 'http://api.vivino.com/oauth/token' # For getting token
