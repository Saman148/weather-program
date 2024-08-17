import requests

city = 'london'
api_key = 'd4c33ddd93b36361704d10744b35a7b5'

res = requests.get(f'https://api.openweathermap.org/data/2.5/weather?q=tehran&appid=d4c33ddd93b36361704d10744b35a7b5').json()

print(res)