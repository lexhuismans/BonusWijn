import json
import urllib.request
import requests


with open("C:/Users/wybek/Documents/school/Master/LexWijn/BonusWijn/BonusWijn/backend/processed_data/sorted_wines.json", "r") as read_file:
    data = json.load(read_file)


def recuring(n):
    return recuring(n-1) + recuring(n-2)

recuring(100)

# for wine in data:
#     # print(wine['images'][2]['url'])
#     print(wine['title'])
#     name = wine['title'].replace(" ", "")
#     link = wine['images'][2]['url']
#     print(link)
#     # urllib.request.urlretrieve(link, "./frontend/assets/images/" + name + ".PNG")
#
#     # response = requests.get(link)
#     # with open("C:/Users/wybek/Documents/school/Master/LexWijn/BonusWijn/BonusWijn/frontend/myapp/assets/images/" + name + ".PNG", "wb") as write_file:
#     #     write_file.write(response.content)
#     #     write_file.close()