import json
import pickle
from pprint import pprint

import ah
import jumbo
import vivino

vivino_data_file = "../vivino_table/vivino_data/name_data_dict_complete_copy.pickle"


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
        print(web_wine["title"])
        # Klaar :)
        formatted_wines.append(web_wine)

    with open(vivino_data_file, "wb") as outfile:
        pickle.dump(wine_dict, outfile)
    return formatted_wines
