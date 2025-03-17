from fastapi import FastAPI
from scraper.scraper import getCryptoData
from fastapi.responses import JSONResponse

app = FastAPI()


@app.get("/cryptos")
async def getCryptos():
    data = getCryptoData()
    if data is not None:
        return JSONResponse(content=data.to_dict(orient="records"))
    else:
        return{"error": "No se pudo obtener datos de las criptomonedas"}