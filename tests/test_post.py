import json

from requests import get, post

url = 'http://127.0.0.1:5000/api/jobs'
correct_json = '{' \
               '"collaborators": "1",' \
               '"end_date": "2020-04-03 03:08",' \
               '"id": 6,' \
               '"is_finished": false,' \
               '"job": "Дельце одно...",' \
               '"start_date": "2020-04-03 03:08",' \
               '"team_leader": 1,' \
               '"work_size": 12' \
               '}'  # Корректный запрос
incorrect_json1 = '{' \
                  '"collaborators": "1",' \
                  '"end_date": "2020-04-03 03:08",' \
                  '"id": 1,' \
                  '"is_finished": false,' \
                  '"job": "Дельце одно...",' \
                  '"start_date": "2020-04-03 03:08",' \
                  '"team_leader": 1,' \
                  '"work_size": 12' \
                  '}'  # Некорректный запрос с существующим id
incorrect_json2 = '{' \
                  '"collaborators": "1",' \
                  '"end_date": "2020-04-03 03:08",' \
                  '"id": 1,' \
                  '"is_finished": false,' \
                  '"job": "Дельце одно...",' \
                  '"start_date": "2020-04-03 03:08",' \
                  '"team_leader": 1' \
                  '}'  # Некорректный запрос не со всеми полями
incorrect_json3 = '{' \
                  '"collaborators": "1",' \
                  '"end_date": "2020-04-03 03:08",' \
                  '"id": 6,' \
                  '"is_finished": "abc",' \
                  '"job": "Дельце одно...",' \
                  '"start_date": "2020-04-03 03:08",' \
                  '"team_leader": "1",' \
                  '"work_size": 12' \
                  '}'  # Некорректный запрос с некорректным типом данных

print(post(url, json=json.loads(correct_json)).json())
print(post(url, json=json.loads(incorrect_json1)).json())
print(post(url, json=json.loads(incorrect_json2)).json())
print(post(url, json=json.loads(incorrect_json3)).json())
print(get(url).json())
