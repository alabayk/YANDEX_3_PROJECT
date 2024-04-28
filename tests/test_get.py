from requests import get


url = 'http://127.0.0.1:5000/api/jobs'
print(get(url).json())
print(get(url + '/1').json())
print(get(url + '/123').json())
print(get(url + '/abc').json())