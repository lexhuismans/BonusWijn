import json


def format_price(price):
    return int(price)/100


with open('./data/jumbo_wijn.json', 'r') as outfile:
    data = json.load(outfile)

all_products = data['products']['data']

wines = []

# Filter products
for product in all_products:
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


bonus_wines = []

# Format products for our Json format
for wine in wines:
    try:
        wine_object = {}

        wine_object['title'] = wine['title']

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

        bonus_wines.append(wine_object)
    except:
        print(wine['title'])

with open('./data/jumbo_filtered_wines.json', 'w') as fout:
    json.dump(bonus_wines, fout)
