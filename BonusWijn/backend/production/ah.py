from supermarktconnector.ah import AHConnector

import math
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


def get_from_query(query='wijn'):
    connector = AHConnector()
    data = search_all_products_ah(connector, size=1000, query=query)

    return data


def format_for_use(wines):
    # format wines for use on website
    formated_wines = []

    for wine in wines:

        wine_object = {}
        store_data = {}
        # filter out non wines
        if "Van Wijngaarden's" in wine['title']:
            continue
        if "De Heidebrouwerij Everzwijn tripel" in wine['title']:
            continue
        if "AH Wijnkado zak" in wine['title']:
            continue
        if 'g' in wine['salesUnitSize']:
            continue
        if wine['mainCategory'] != 'Wijn en bubbels':
            continue

        wine_object['title'] = wine['title'].strip()

        # images
        try:
            store_data['images'] = wine['images'][-2]
        except:
            continue

        wine_object['store'] =  wine['shopType']
        store_data['volume'] = wine['salesUnitSize']
        try:
            if wine['isBonus']:
                store_data['bonus'] = True
                if wine['promotionType'] == 'NATIONAL' or wine['promotionType']== "PERPETUAL" or wine['promotionType'] =="GALL":
                    store_data['promotion_type'] = 'normal'
                elif wine['promotionType'] == 'AHONLINE':
                    store_data['promotion_type'] = "AHONLINE"
                elif wine['promotionType'] == "GALLCARD":
                    store_data['promotion_type'] = "GALLCARD"
                else:
                    store_data['promotion_type'] = "none"

                if wine['bonusMechanism'] == '2E HALVE PRIJS':
                    store_data['original_price_per_fles'] = wine['priceBeforeBonus']
                    store_data['bonus_price_per_fles'] = 1.5*wine['priceBeforeBonus']
                    store_data['amount_of_bottles'] = 2
                elif wine['bonusMechanism'] == "2=1":
                    store_data['original_price_per_fles'] = wine['priceBeforeBonus']
                    store_data['bonus_price_per_fles'] = wine['priceBeforeBonus']
                    store_data['amount_of_bottles'] = 2
                elif wine['bonusMechanism'] == "-10% VANAF 6 STUKS":
                    store_data['original_price_per_fles'] = wine['priceBeforeBonus']
                    store_data['bonus_price_per_fles'] = 0.9*wine['priceBeforeBonus']
                    store_data['amount_of_bottles'] = 6
                elif wine['bonusMechanism'] == 'BONUS' and "6 x" in wine['salesUnitSize']:
                    store_data['original_price_per_fles'] = wine['priceBeforeBonus']
                    store_data['bonus_price_per_fles'] = wine['currentPrice']
                    store_data['amount_of_bottles'] = 6
                elif "6 x" in wine['salesUnitSize']:
                    store_data['original_price_per_fles'] = wine['priceBeforeBonus']
                    store_data['bonus_price_per_fles'] = wine['currentPrice']
                    store_data['amount_of_bottles'] = 6
                else:
                    store_data['original_price_per_fles'] = wine['priceBeforeBonus']
                    store_data['bonus_price_per_fles'] = wine['currentPrice']
                    store_data['amount_of_bottles'] = 1

            else:
                store_data['bonus'] = False
                if "6 x" in wine['salesUnitSize']:
                    store_data['original_price'] = wine['priceBeforeBonus']
                    store_data['amount_of_bottles'] = 6
                else:
                    print(wine)
                    store_data['original_price'] = wine['priceBeforeBonus']
                    store_data['amount_of_bottles'] = 1
        except:
            store_data['bonus'] = False
            if "6 x" in wine['salesUnitSize']:
                store_data['original_price_per_fles'] = wine['priceBeforeBonus']
                store_data['amount_of_bottles'] = 6
            else:
                store_data['original_price_per_fles'] = wine['priceBeforeBonus']
                store_data['amount_of_bottles'] = 1

        wine_object['store_data'] = store_data
        formated_wines.append(wine_object)

    return formated_wines
