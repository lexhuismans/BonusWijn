import json
import csv
import pickle


with open('./data/ah_wijn.json', 'r') as outfile:
    data = json.load(outfile)

all_products = data['products']

wines = []

for product in all_products:
    try:
        if product['salesUnitSize'] == '0,75 l' and product['mainCategory'] == 'Wijn en bubbels' and product[
            'promotionType'] == 'GALL':
            wines.append(product)

        elif product['salesUnitSize'] == '0,75 l' and product['mainCategory'] == 'Wijn en bubbels' and product[
            'promotionType'] == 'NATIONAL':
            wines.append(product)
    except:
        pass



bonus_wines = []

for wine in wines:
    try:
        wine_object = {}
        wine_object['title'] = wine['title']
        wine_object['images'] = wine['images']
        wine_object['store'] = wine['shopType']
        wine_object['bottleSize'] = wine['salesUnitSize']
        if wine['bonusMechanism'] == "2E HALVE PRIJS":
            wine_object['amountOfBottles'] = 2
            wine_object['originalPrice'] = 2*wine['priceBeforeBonus']
            wine_object['bonusPrice'] = 1.5*wine['priceBeforeBonus']
        elif "2 VOOR" in wine['bonusMechanism']:
            wine_object['amountOfBottles'] = 2
            new_price = wine['bonusMechanism'].split(" ")[2]
            wine_object['originalPrice'] = 2 * wine['priceBeforeBonus']
            wine_object['bonusPrice'] = new_price
        else:
            wine_object['amountOfBottles'] = 1
            wine_object['originalPrice'] = wine['priceBeforeBonus']
            wine_object['bonusPrice'] = wine['currentPrice']
        bonus_wines.append(wine_object)
    except:
        print(wine)

with open('./data/filtered_wines.json', 'w') as fout:
    json.dump(bonus_wines , fout)