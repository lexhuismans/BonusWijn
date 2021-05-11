import json
import urllib.request
import requests


with open("C:/Users/wybek/Documents/school/Master/LexWijn/BonusWijn/BonusWijn/backend/processed_data/sorted_wines.json", "r") as read_file:
    data = json.load(read_file)




for wine in data:
    print(wine['title'])
    name = wine['title'].replace(" ", "")
    link = wine['images'][1]['url']
    print(link)
    response = requests.get(link)
    with open("C:/Users/wybek/Documents/school/Master/LexWijn/BonusWijn/BonusWijn/frontend/myapp/assets/images/" + name + ".PNG", "wb") as write_file:
        write_file.write(response.content)
        write_file.close()