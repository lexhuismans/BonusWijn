from supermarktconnector.ah import AHConnector
import requests

connector = AHConnector()
#print(connector.get_categories())

HEADERS = {
    'User-Agent': 'android/6.29.3 Model/phone Android/7.0-API24',
    'Host': 'ms.ah.nl',
}

response = requests.post(
            'https://ms.ah.nl/create-anonymous-member-token',
            headers=HEADERS,
            params={"client": "appie-anonymous"}
        )

token = response.json()

response = requests.get(
            'https://ms.ah.nl/mobile-services/v1/product-shelves/categories',
            headers={**HEADERS, "Authorization": "Bearer {}".format(token.get('access_token'))}
        )
print(response.text)
print('JSON')
print(response.json())
