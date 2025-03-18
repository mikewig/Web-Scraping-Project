from fastapi import FastAPI
import pandas as pd
from pydantic import BaseModel
from fastapi.responses import StreamingResponse

from market import fetch_cryptocurrencies
from charts import createCharts

app = FastAPI()

class cryptoResponse(BaseModel):
    name: str
    symbol: str
    price: float

@app.get('/cryptos', response_model=list[cryptoResponse])
async def get_cryptocurrencies():
    try:
        data = fetch_cryptocurrencies()
        crypto_data = []

        for item in data['data']:
            crypto_data.append({
                'name': item['name'],
                'symbol': item['symbol'],
                'price': item['quote']['USD']['price']
            })

        df = pd.DataFrame(crypto_data)


        buf = createCharts(df)

        return StreamingResponse(buf, media_type='image/png')
    
    except Exception as e:
        return {"error": str(e)}

         