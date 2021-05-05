from supermarktconnector.jumbo import JumboConnector

import math
import json


def get_all_from_query(query):
    connector = JumboConnector()

    size = 30
    response = connector.search_products(query=query, page=0, size=size)

    for i in range(1, math.ceil(response['products']['total'] / size)):
        new_response = connector.search_products(query='wijn', page=i, size=size)
        response['products']['data'] = response['products']['data'] + new_response['products']['data']

    return response


response = get_all_from_query('wijn')
with open('./data/jumbo_wijn.json', 'w') as outfile:
    json.dump(response, outfile)
