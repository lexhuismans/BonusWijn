from supermarktconnector.ah import AHConnector
import json


connector = AHConnector()

response = connector.search_products(query='wijn', size=5000, page=0)

with open('./data/ah_wijn.json', 'w') as outfile:
    json.dump(response, outfile)


