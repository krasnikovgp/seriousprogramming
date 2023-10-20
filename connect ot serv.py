import requests

URL = 'http://1060.ru'

response = requests.get(URL)

print(response)
print(response.status_code)
print(response.headers)

for item in response.headers:
    print(item)

print(response.content)
print(response.text)