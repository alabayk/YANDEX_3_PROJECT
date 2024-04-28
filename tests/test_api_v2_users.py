import json

import requests

url1 = "http://127.0.0.1:5000/api/v2/users/1"
url2 = "http://127.0.0.1:5000/api/v2/users/123"
url3 = "http://127.0.0.1:5000/api/v2/users"

print(requests.get(url1).json())
print(requests.get(url2).json())

requests.delete(url1)

requests.post(url3,
              headers={'Content-Type': 'application/json'},
              data='{"address": "Строителей, 23Б, 58",'
                   '"age": 18,'
                   '"email": "sia.ilya.2017@gmail.com",'
                   '"hashed_password": "pbkdf2:sha256:150000$f48LP1uA$05169e9f46954b79d896a5213c5c393ebf2d286047439c86e85b933107e1934a",'
                   '"name": "Илья",'
                   '"position": "Колонист",'
                   '"speciality": "Маг",'
                   '"surname": "Самойлов"'
                   '}'.encode('utf-8'))

print(requests.get(url3).json())