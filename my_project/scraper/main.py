# from fastapi import FastAPI
# from pydantic import BaseModel
# import requests
# from typing import Optional
# from models.database import Crypto
# from db import Session

# app = FastAPI()

# API_URL = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'

# API_KEY = '711ceffc-6d4a-4fa7-870f-0e6d48df306f'

# parameters = {
#     'start': '1',
#     'limit': '10',
#     'convert': 'USD'
# }

# headers = {
#     'Accepts': 'aplication/json',
#     'X-CMC_PRO_API_KEY': API_KEY
# }

# def fetch_cryptocurrencies():
#     response = requests.get(API_URL, params=parameters, headers=headers)

#     if response.status_code == 200:
#         return response.json()
#     else:
#         raise Exception(f"Failed to get data: {response.status_code}")

# class cryptoResponse(BaseModel):
#     name: str
#     abbreviation: str
#     price: float
#     symbol: Optional[str] = None

# def saveCryptoCurrencies(db, data):
#     for item in data['data']:
#         crypto = Crypto(
#             name=item['name'],
#             abbreviation=item['symbol'],
#             price=item['quote']['USD']['price']
#         )
#         db.add(crypto)
#     db.commit()


# @app.get('/cryptos', response_model=list[cryptoResponse])
# async def get_cryptocurrencies():
#     db = Session()
#     try:
#         data = fetch_cryptocurrencies()
#         saveCryptoCurrencies(db, data)
#         crypto_data = [
#             {
#                 'name': item['name'],
#                 'abbreviation': item['symbol'],
#                 'price': item['quote']['USD']['price']
#             } for item in data['data']
#         ]
#         return crypto_data
    
#     except Exception as e:
#         return {"error": str(e)}
    
#     finally:
#         db.close()
    