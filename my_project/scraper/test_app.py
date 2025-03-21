from fastapi.testclient import TestClient
from scraper.main import app
import pytest
from unittest.mock import patch

client = TestClient(app)

@pytest.fixture
def test_GetCryptoCurrencies():
    response = client.get("/cryptos")
    assert response.status_code == 200
    assert response.headers["content-type"] == "image/png"
    

def test_GetCryptoErrors():

    from market import fetch_cryptocurrencies

    with patch('app.market.fetch_cryptocurrencies') as mock_fetch:
        mock_fetch.side_effect = Exception("Error al obtener criptomonedas")

        response = client.get("/cryptos")

        assert response.status_code == 200
        assert response.json() == {"error": "Error al obtener criptomonedas"}