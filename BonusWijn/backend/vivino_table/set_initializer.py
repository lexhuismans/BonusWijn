import pickle



wine_dictionary = dict()

with open('./vivino_data/name_data_dict.pickle', 'wb') as handle:
    pickle.dump(wine_dictionary, handle)

