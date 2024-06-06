"""
curl -X 'PUT' \
  'http://5.63.153.31:5051/v1/account/7d87f459-e627-4917-873f-729d0f855515' \
  -H 'accept: text/plain'
}'

"""
import pprint

import requests

# url = 'http://5.63.153.31:5051/v1/account'
# headers = {
#     'accept': '*/*',
#     'Content-Type': 'application/json'
# }
# json = {
#     "login": "medvedeva_test1",
#     "email": "medvedeva_test1@mail.ru",
#     "password": "123456789"
# }
# response = requests.post(
#     url=url,
#     headers=headers,
#     json=json
# )

url = 'http://5.63.153.31:5051/v1/account/7d87f459-e627-4917-873f-729d0f855515'
headers = {
    'accept': 'text/plain'
}
response = requests.put(
    url=url,
    headers=headers
)
print(response.status_code)
pprint.pprint(response.json())
response.json = (response.json())
print(response.json['resource']['rating']['quantity'])
