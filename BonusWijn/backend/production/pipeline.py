import json
import pickle
import random
from pprint import pprint

import requests

import ah
import jumbo
import vivino

vivino_data_file = "./files_in/name_data_dict_complete_copy.pickle"


def make_jumbo(wines=None):
    # Get all wine Jumbo
    if wines is None:
        wines = jumbo.get_all_from_query()

    with open(vivino_data_file, "rb") as handle:
        wine_dict = pickle.load(handle)

    formatted_wines = []
    for wine in wines:
        web_wine = {}
        # Filter out crazy wines zoals 'azijn'
        # format it to {title: 'title', store: 'jumbo', store_data: 'jumbo data'}
        skip_list = [
            "saus",
            "mosselen",
            "kees",
            "mosterd",
            "azijn",
            "zuurkool",
            "kruiden",
            "spijs",
            "pakket",
            "boek",
        ]
        if any(x in wine["title"].lower() for x in skip_list):
            continue

        web_wine["title"] = wine["title"]
        web_wine["store"] = "Jumbo"

        jumbo_formatted = jumbo.format_for_use(wine)
        if jumbo_formatted is None:
            continue
        web_wine["store_data"] = jumbo.format_for_use(wine)

        # Add vivino data
        web_wine["vivino"] = vivino.find_title(wine["title"], wine_dict)

        # Filter title
        remove_list = [
            "–",
            "-",
            ",",
            "liter",
            "Liter",
            "ml",
            "cl",
            "ML",
            "Ml",
            "1,5L",
            "750",
            "75",
            "0,75",
            "700",
            "500",
            "375",
            "275",
            "250",
            "200",
            "187",
            "100",
            "15L",
            "1L",
            "3",
            "8 x",
            "6 x",
            "6x",
            "3L",
            "25L",
            "4 x",
            "12",
            " x ",
            "xx",
        ]
        for x in remove_list:
            web_wine["title"] = web_wine["title"].replace(x, "")
        web_wine["title"] = web_wine["title"].replace("  ", " ").strip()

        # Klaar :)
        formatted_wines.append(web_wine)

    with open(vivino_data_file, "wb") as outfile:
        pickle.dump(wine_dict, outfile)
    return formatted_wines


def make_AH(wines=None):
    # Get all wine AH
    if wines is None:
        wines = ah.get_all_from_query()

    # Format from AH
    formatted_wines = ah.format_for_use(wines)

    # Add vivino data
    with open(vivino_data_file, "rb") as handle:
        wine_dict = pickle.load(handle)
    
    for wine in formatted_wines:
        wine['vivino'] = vivino.find_title(wine['title'], wine_dict)

    with open(vivino_data_file, "wb") as outfile:
        pickle.dump(wine_dict, outfile)

    return formatted_wines

def get_images(wines):
    """
    Get all the images from a formatted wines list. 
    """
    # Add check if outfile is already in!
    for wine in wines:
        name = wine['title'].replace(" ", "")
        try:
            link = wine['store_data']['images']['url']
        except TypeError:
            linke = wine['store_data']['images'][0]['url']
        response = requests.get(link)
        file_path = "./files_out/images/" + name + ".png"
        with open(file_path, "wb") as write_file:
            write_file.write(response.content)

