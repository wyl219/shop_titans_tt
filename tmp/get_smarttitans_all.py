BASE_URL=r'https://smartytitans.com/'
API_URL=r'api/item/last/all'

import requests
import json


a=requests.get(BASE_URL+API_URL)
print(a.text)
json.dump(a.json(), open('../list_all.json', 'w'), indent=4)
print(a.status_code)