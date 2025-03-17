import pytest
from unittest.mock import patch, MagicMock
from scraper.scraper import getCryptoData


@pytest.fixture
def mock_request_get():
    with patch('requests.get') as mock_get:
        yield mock_get


def test_getCryptoData(mock_request_get):
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.content = b"""
    <table>
        <tr class="coin-item">
            <div class="tw-text-gray-700 dark:tw-text-moon-100">BTC</div>
            <span class="data-prev-price">50,000 USD</span>
            <span class="data-price-btc">+5%</span>
            <span class="data-prev-price">900B</span>
        </tr>
    </table>
    """

    mock_request_get.return_value = mock_response


    df = getCryptoData()

    print(df)

    assert df is not None
    assert len(df) == 1
    assert df['Nombre'][0] == "BTC"
    assert df['Precio'][0] == "50,000 USD"
    assert df['Cambio 24h'][0] == "+5%"
    assert df['Capitalización de mercado'][0] == "900B"