from supermarktconnector.jumbo import JumboConnector

import time
import math
import json
import pprint

connector = JumboConnector()

size = 30
response = connector.search_products(query='wijn', page=0, size=size)

wine_n = 0
for i in range(1, math.ceil(response['products']['total'] / size)):
    new_response = connector.search_products(query='wijn', page=i, size=size)
    response['products']['data'] = response['products']['data'] + new_response['products']['data']


with open('./data/jumbo_wijn.json', 'w') as outfile:
    json.dump(response, outfile)
