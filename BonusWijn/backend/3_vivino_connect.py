import json
import urllib.request
import time
# import unicodedata
import unidecode



with open("./data/filtered_wines.json", "r") as read_file:
    data = json.load(read_file)


combined_data = []
for wine in data:

    title = wine['title']
    temp = title.replace(" ", "+")
    link = u"https://www.vivino.com/search/wines?q=" + temp
    normalided_link = unidecode.unidecode(link)
    try:
        time.sleep(2)

        response = urllib.request.urlopen(normalided_link)

        response = response.read()

        response = response.decode("utf-8")

        response = response.split("\n")


        for index, val in enumerate(response):
            if val == 'Gemiddelde beoordeling':
                wine['rating'] = response[index + 3]
                wine['numberOfReviews'] = int(response[index + 15].split(" ")[0])
                combined_data.append(wine)
                break
    except:
        print(response)
        print(normalided_link)

with open('./processed_data/ah_vivino_wines.json', 'w') as fout:
    json.dump(combined_data , fout)