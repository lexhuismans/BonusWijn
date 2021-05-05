import jumbo
import vivino
import json


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


def plus_pipeline():
    pass
