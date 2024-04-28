import json

from requests import get, post, delete, put

url = 'http://127.0.0.1:5000/api/jobs'

print(put(url + '/4',
          json={"job": "Самая лучшая работа!"},
          headers={'Content-Type': "application/json", 'Accept': "application/json"}).json())
print(put(url + '/4',
          json={"random key": "value"},
          headers={'Content-Type': "application/json", 'Accept': "application/json"}).json())
print(put(url + '/404',
          json={"job": "value"},
          headers={'Content-Type': "application/json", 'Accept': "application/json"}).json())
print(put(url + '/abc',
          json={"job": "value"},
          headers={'Content-Type': "application/json", 'Accept': "application/json"}).json())
print(get(url).json())

