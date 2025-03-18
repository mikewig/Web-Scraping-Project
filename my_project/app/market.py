import requests

API_URL = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'

API_KEY = '711ceffc-6d4a-4fa7-870f-0e6d48df306f'

parameters = {
    'start': '1',
    'limit': '10',
    'convert': 'USD'
}

headers = {
    'Accepts': 'aplication/json',
    'X-CMC_PRO_API_KEY': API_KEY
}

def fetch_cryptocurrencies():
    response = requests.get(API_URL, params=parameters, headers=headers)

    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Failed to get data: {response.status_code}")