from supermarktconnector.ah import AHConnector
import json


def search_all_products_ah(connector, size, query):
    """
    Iterate all the products available, filtering by query or other filters. Will return generator.
    :param kwargs: See params of 'search_products' method, note that size should not be altered to optimize/limit pages
    :return: generator yielding products
    """
    wines = []
    response = connector.search_products(page=0, query=query, size=size)
    for wine in response['products']:
        wines.append(wine)

    for page in range(1, response['page']['totalPages']):
        response = connector.search_products(page=page, query=query, size=size)
        for wine in response['products']:
            wines.append(wine)

    return wines


connector = AHConnector()

# response = connector.search_products(query='wijn', size=5000, page=0)
all_wines = search_all_products_ah(connector, size=1000, query='wijn')

with open('./ah_name_data/ah_wines.json', 'w') as outfile:
    json.dump(all_wines, outfile)


