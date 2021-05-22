from supermarktconnector.jumbo import JumboConnector

import math
import json


def format_price(price):
    return int(price)/100


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
    
    # Return json response
    return response


def format_for_use(store_data):
    '''
    Format so it can be used on the website.
    Makes a new JSON with only the needed features.

    Params
    ------
    store_data : 
        json with store data
    Returns
    -------
    formated_wines : json
        json file with right format for website.
    '''

    wine_object = {}

    # images
    wine_object['images'] = store_data['imageInfo']['primaryView']

    # bottle size
    if store_data['quantity'] in ['750 ml', '75 cl', '750 ml.', '0,75 i', '75 cl.', '0,75 liter']:
        wine_object['bottleSize'] = "0,75 l"
    elif store_data['quantity'] == '250 ml' or store_data['quantity'] == '250.0 ml':
        wine_object['bottleSize'] = "0,25 l"
    elif store_data['quantity'] == '1500.0 ml':
        wine_object['bottleSize'] = '1,5 l'
    elif store_data['quantity'] == '6 x 750 ml' or store_data['quantity'] == '6 x 75 cl':
        wine_object['bottleSize'] = '6 x 0,75 l'
    elif store_data['quantity'] == '6 x 6000.0 ml':
        wine_object['bottleSize'] = '6 x 1 l'
    elif store_data['quantity'] == '20 cl':
        wine_object['bottleSize'] = '0,2 l'
    elif store_data['quantity'] == '1 l':
        wine_object['bottleSize'] = '1 l'
    elif store_data['quantity'] == '375 ml' or store_data['quantity'] == '37,5 cl' or store_data['quantity'] == '375 ml.':
        wine_object['bottleSize'] = '0,375 l'
    else:
        print('skip: ', store_data['title'])
        return None

    # Prices
    price = format_price(store_data['prices']['price']['amount'])
    wine_object['originalPrice'] = price
    wine_object['amountOfBottles'] = 1
    
    # Promotion
    if 'promotion' in store_data:
        promotion = store_data['promotion']['tags'][0]['text']
        if promotion == 'Alleen online':
            wine_object['promotionType'] = 'online'
            promotion = store_data['promotion']['tags'][1]['text']
        else:
            wine_object['promotionType'] = 'normal'
        if promotion == '3 halen, 2 betalen':
            wine_object['bonusPrice'] = 2 * price / 3
            wine_object['amountOfBottles'] = 3
        elif promotion == '2 halen, 1 betalen':
            wine_object['bonusPrice'] = price / 2
            wine_object['amountOfBottles'] = 2
        elif promotion == "2 voor 7,99 euro":
            wine_object['bonusPrice'] = 7.99 / 2
            wine_object['amountOfBottles'] = 2
        elif promotion == '3 voor 10,00 euro':
            wine_object['bonusPrice'] = 10 / 3
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
        elif promotion == '10% korting':
            wine_object['bonusPrice'] = price * .9
            wine_object['amountOfBottles'] = 1
        elif promotion == '25% korting':
            wine_object['bonusPrice'] = price * .75
            wine_object['amountOfBottles'] = 1
        elif promotion == '50% korting':
            wine_object['bonusPrice'] = price * .5
            wine_object['amountOfBottles'] = 1
        elif promotion == '4 halen 2 betalen':
            wine_object['bonusPrice'] = price * 2
            wine_object['amountOfBottles'] = 4
        else:
            print('Promotion niet gevonden:')
            print(promotion)
    else:
        wine_object['promotionType'] = 'None'
    
    if '6 x' in store_data['title'] or '6x' in store_data['title']:
        wine_object['amountOfBottles'] = 6

    return wine_object