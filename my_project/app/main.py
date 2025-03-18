from fastapi import FastAPI
import pandas as pd
import requests
from pydantic import BaseModel
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import io
from fastapi.responses import StreamingResponse

app = FastAPI()

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

class cryptoResponse(BaseModel):
    name: str
    symbol: str
    price: float

@app.get('/cryptos', response_model=list[cryptoResponse])
async def get_cryptocurrencies():
    response = requests.get(API_URL, params=parameters, headers=headers)

    if response.status_code == 200:
        data = response.json()
        
        crypto_data = []
        for item in data['data']:
            crypto_data.append({
                'name': item['name'],
                'symbol': item['symbol'],
                'price': item['quote']['USD']['price']
            })

        df = pd.DataFrame(crypto_data)

        fig, ax = plt.subplots(figsize=(10,6))
        for i, row in df.iterrows():
            ax.plot([0, 1], [row['price'], row['price']], label=row['name'])

        ax.set_title('Price of the popular cryptos')
        ax.set_xlabel('Índice')
        ax.set_ylabel('Price in USD')
        ax.legend(loc='upper left')
        
        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        buf.seek(0)
        
        return StreamingResponse(buf, media_type="image/png")
    else:
        return {"error": "Failed to fetch data from CoinMarketCap API", "status_code": response.status_code} 