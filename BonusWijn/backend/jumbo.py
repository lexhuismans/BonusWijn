from supermarktconnector.jumbo import JumboConnector

import math
import json


def get_all_from_query(query='wijn'):
    '''
    Get all the items from a search query.
    '''
    connector = JumboConnector()

    size = 30
    response = connector.search_products(query=query, page=0, size=size)

    for i in range(1, math.ceil(response['products']['total'] / size)):
        new_response = connector.search_products(query='wijn', page=i, size=size)
        response['products']['data'] = response['products']['data'] + new_response['products']['data']

    response = response['products']['data']
    # Save result in file
    
    with open('./data/jumbo_wijn.json', 'w') as outfile:
        json.dump(response, outfile)
    
    # Return json response
    return response


def format_price(price):
    return int(price)/100


def filter_products_jumbo(data):
    '''
    Filter wine from Jumbo json. 
    Params
    ------
    data : json
        json file with data as retreived from Jumbo.
    Returns
    -------
    wines : json
        wines filtered for size/promotion etc.
    '''

    wines = []
    # Filter products
    for product in data:
        try:
            if (product['quantity'] == '750 ml' or product['quantity'] == '75 cl'):

                # Check if online
                try:
                    if product['promotion']['additionalTag']:
                        if not product['promotion']['additionalTag'] == 'Alleen online':
                            wines.append(product)
                except:
                    wines.append(product)
        except:
            pass

    return wines


def format_for_use(wines):
    '''
    Format so it can be used on the website.
    Makes a new JSON with only the needed features.

    Params
    ------
    wines : json
        json file with all the wines as from Jubmo website.
    Returns
    -------
    formated_wines : json
        json file with right format for website.
    '''
    formated_wines = []

    # Format products for our Json format
    for wine in wines:
        try:
            wine_object = {}

            wine_object['title'] = wine['title'].replace('-','').replace('750ML', '').replace('750Ml', '').replace('750ML', '').strip()

            # images
            wine_object['images'] = wine['imageInfo']['primaryView']
            wine_object['store'] = 'Jumbo'

            # bottle size
            if wine['quantity'] == '750 ml' or wine['quantity'] == '75 cl':
                wine_object['bottleSize'] = "0,75 l"

            # Prices
            price = format_price(wine['prices']['price']['amount'])
            wine_object['originalPrice'] = price

            promotion = wine['promotion']['tags'][0]['text']
            if promotion == '3 halen, 2 betalen':
                wine_object['bonusPrice'] = 2 * price
                wine_object['amountOfBottles'] = 3
            elif promotion == '2 halen, 1 betalen':
                wine_object['bonusPrice'] = price
                wine_object['amountOfBottles'] = 2
            elif promotion == '3 voor 10,00 euro':
                wine_object['bonusPrice'] = 10
                wine_object['amountOfBottles'] = 3
            elif promotion == '1 voor 4,49 euro':
                wine_object['bonusPrice'] = 4.49
                wine_object['amountOfBottles'] = 1
            elif promotion == '1 voor 2,99 euro':
                wine_object['bonusPrice'] = 2.99
                wine_object['amountOfBottles'] = 1
            elif promotion == '1 voor 6,99 euro':
                wine_object['bonusPrice'] = 6.99
                wine_object['amountOfBottles'] = 1
            wine_object['pricePerBottle'] = wine_object['bonusPrice']/wine_object['amountOfBottles']

            formated_wines.append(wine_object)
        except:
            print(wine['title'])

    return formated_wines
