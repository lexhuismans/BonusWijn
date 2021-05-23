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
    if 'quantity' in store_data:
        if store_data['quantity'] in ['750 ml', '75 cl', '750 ml.', '0,75 i', '75 cl.', '0,75 liter', '0,75 l', '750.0 ml', '0.75 liter']:
            wine_object['volume'] = "0,75 l"
        elif store_data['quantity'] in ['250 ml', '250.0 ml', '25 cl.']:
            wine_object['volume'] = "0,25 l"
        elif store_data['quantity'] == '1500.0 ml':
            wine_object['volume'] = '1,5 l'
        elif store_data['quantity'] in ['6 x 750 ml', '6 x 75 cl', '6 x 0,75 l']:
            wine_object['volume'] = '6 x 0,75 l'
        elif store_data['quantity'] in ['6 x 6000.0 ml', '6 x 1 l']:
            wine_object['volume'] = '6 x 1 l'
        elif store_data['quantity'] in ['50 cl']:
            wine_object['volume'] = '0,5 l'
        elif store_data['quantity'] == '20 cl':
            wine_object['volume'] = '0,2 l'
        elif store_data['quantity'] in ['18.7 cl']:
            wine_object['quantity'] = '0,187 l'
        elif store_data['quantity'] == '1 l':
            wine_object['volume'] = '1 l'
        elif store_data['quantity'] in ['375 ml', '37,5 cl', '375 ml.']:
            wine_object['volume'] = '0,375 l'
        #else:
            #print('Skip: ', store_data['title'])
    else:
        print('No quantity: ', store_data['title'])
        return None

    # Prices
    price = format_price(store_data['prices']['price']['amount'])
    wine_object['original_price_per_fles'] = price
    wine_object['amount_of_bottles'] = 1
    
    # Promotion
    if 'promotion' in store_data:
        wine_object['bonus'] = True
        promotion = store_data['promotion']['tags'][0]['text']
        if promotion == 'Alleen online':
            wine_object['promotionType'] = 'online'
            promotion = store_data['promotion']['tags'][1]['text']
        else:
            wine_object['promotionType'] = 'normal'
        if promotion == '3 halen, 2 betalen':
            wine_object['bonus_price_per_fles'] = 2 * price / 3
            wine_object['amount_of_bottles'] = 3
        elif promotion == '2 halen, 1 betalen':
            wine_object['bonus_price_per_fles'] = price / 2
            wine_object['amount_of_bottles'] = 2
        elif promotion == "2 voor 7,99 euro":
            wine_object['bonus_price_per_fles'] = 7.99 / 2
            wine_object['amount_of_bottles'] = 2
        elif promotion == '3 voor 10,00 euro':
            wine_object['bonus_price_per_fles'] = 10 / 3
            wine_object['amount_of_bottles'] = 3
        elif promotion == '1 voor 4,49 euro':
            wine_object['bonus_price_per_fles'] = 4.49
            wine_object['amount_of_bottles'] = 1
        elif promotion == '1 voor 2,99 euro':
            wine_object['bonus_price_per_fles'] = 2.99
            wine_object['amount_of_bottles'] = 1
        elif promotion == '1 voor 6,99 euro':
            wine_object['bonus_price_per_fles'] = 6.99
            wine_object['amount_of_bottles'] = 1
        elif promotion == '10% korting':
            wine_object['bonus_price_per_fles'] = price * .9
            wine_object['amount_of_bottles'] = 1
        elif promotion == '25% korting':
            wine_object['bonus_price_per_fles'] = price * .75
            wine_object['amount_of_bottles'] = 1
        elif promotion == '50% korting':
            wine_object['bonus_price_per_fles'] = price * .5
            wine_object['amount_of_bottles'] = 1
        elif promotion == '4 halen 2 betalen':
            wine_object['bonus_price_per_fles'] = price * 2 / 4
            wine_object['amount_of_bottles'] = 4
        else:
            print('Promotion niet gevonden:')
            print(promotion)
    else:
        wine_object['bonus'] = False
    
    if '6 x' in store_data['title'] or '6x' in store_data['title']:
        wine_object['amount_of_bottles'] = 6

    return wine_object