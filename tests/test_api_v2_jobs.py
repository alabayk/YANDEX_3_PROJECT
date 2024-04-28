import json

import requests

url1 = "http://127.0.0.1:5000/api/v2/jobs/1"
url2 = "http://127.0.0.1:5000/api/v2/jobs/123"
url3 = "http://127.0.0.1:5000/api/v2/jobs"

print(requests.get(url1).json())
print(requests.get(url2).json())

requests.delete(url1)

requests.post(url3,
              headers={'Content-Type': 'application/json'},
              data='{'
                   '"collaborators": "2, 3",'
                   '"is_finished": false,'
                   '"job": "Построить что-нибудь",'
                   '"start_date": "2020-03-30 19:03",'
                   '"team_leader": 1,'
                   '"work_size": 10'
                   '}'.encode('utf-8'))

print(requests.get(url3).json())
