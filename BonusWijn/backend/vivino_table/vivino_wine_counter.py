import json
import pickle



with open('./vivino_data/name_data_dict_complete_copy.pickle', 'rb') as handle:
    wine_name_dict = pickle.load(handle)


print(len(wine_name_dict.keys()))
#
# for wine in wine_name_dict.keys():
#     print(wine_name_dict[wine])