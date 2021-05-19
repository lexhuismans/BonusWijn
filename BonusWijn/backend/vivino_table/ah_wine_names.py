from supermarktconnector.ah import AHConnector
import json


connector = AHConnector()

response = connector.search_products(query='wijn', size=5000, page=0)

with open('./ah_name_data/ah_wines.json', 'w') as outfile:
    json.dump(response, outfile)


