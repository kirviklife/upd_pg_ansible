import requests

# Токен API
token = 'APY0SWVwIr9FwzOp1GQfTu5a9mPr68uWsrXcAXX2cZaWFwOWzSGCeFhLd2DQlopFpqpB1'

# Адрес API
url = 'https://api.apyhub.com/data/dictionary/country'

headers = {
    'apy-token': token,
    'Accept': 'application/json',
    'Content-Type': 'application/json'
}


response = requests.get(url, headers=headers, verify=False)

if response.status_code == 200:
    print([0, response.json()])
else:
    print([-1,'(%s) %s'%(response.status_code,response.text)])