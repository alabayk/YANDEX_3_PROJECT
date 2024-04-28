from requests import get, post, delete

url = 'http://127.0.0.1:5000/api/jobs'

print(delete(url + '/5').json())  # Корректный запрос
print(delete(url + '/123').json())  # Несуществующий id
print(delete(url + '/abc').json())  # Некорректный id
print(get(url).json())
