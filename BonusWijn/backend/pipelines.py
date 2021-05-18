import jumbo
import vivino
import json

import requests


# ----------------
# AH pipeline
# ----------------

# Jumbo pipeline
def jumbo_pipeline():
    data = jumbo.get_all_from_query()  # Get all wines from jumbo

    # Filter wines
    wines = jumbo.filter_products_jumbo(data)
    formated_wines = jumbo.format_for_use(wines)

    with open('./data/jumbo_filtered_wines.json', 'w') as fout:
        json.dump(formated_wines, fout)

    # Add vivino ratings
    vivino.add_vivino_data("./data/jumbo_filtered_wines.json")


# Filter title by removing redundant tokens etc.
def filter_title(js):
    '''
    js : json 
        json with all wines
    '''
    for wine in js:
        wine['title'] = wine['title'].replace('-', '').replace('750ML', '').replace('750Ml', '').strip()
        wine['title'] = wine['title'].replace('  ', ' ')
    return js 


def get_images(data):
    for wine in data:
        name = wine['title'].replace(" ", "")
        link = wine['images'][0]['url']
        response = requests.get(link)

        with open("/Users/Lex/Desktop/Software Projects/Wijnhandel/BonusWijn/BonusWijn/frontend/myapp/assets/images/" + name + ".PNG", "wb") as write_file:
            write_file.write(response.content)
            write_file.close()


def plus_pipeline():
    pass


if __name__ == '__main__':
    with open('./processed_data/jumbo_vivino_wines.json', 'r+') as file:
        data = json.load(file)
        get_images(data)