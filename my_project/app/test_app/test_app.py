from fastapi.testclient import TestClient
from app.main import app
from unittest.mock import patch
import pandas as pd

client = TestClient(app)

def test_GetCryptos():
    with patch('scraper.scraper.getCryptoData') as mock_getCryptoData:
        mock_getCryptoData.return_value = pd.DataFrame({
            "Nombre": ["BTC"],
            "Precio": ["50,000 USD"],
            "Cambio 24h": ["+5%"],
            "Capitalización de mercado": ["900B"]
        })


        response = client.get("/cryptos")
        
        print(response.json())


        assert response.status_code == 200
        assert len(response.json()) == 1
        assert response.json()[0]["Nombre"] == "BTC"
        assert response.json()[0]["Precio"] == "50,000 USD"
        assert response.json()[0]["Cambio 24h"] == "+5%"
        assert response.json()[0]["Capitalización de mercado"] == "900B"