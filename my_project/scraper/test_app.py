import pytest
from unittest.mock import patch, MagicMock
import os
import scraper.crypto_scraper

@pytest.fixture
def sample_crypto_data():
    return [
        {'name': 'Bitcoin', 'symbol': 'BTC', 'price': 60000.0},
        {'name': 'Ethereum', 'symbol': 'ETH', 'price': 3000.0}
    ]

@patch('mysql.connector.connect')
def test_setup_db(mock_connect):
    mock_cursor = MagicMock()
    mock_connection = MagicMock()
    mock_connection.cursor.return_value = mock_cursor
    mock_connect.return_value = mock_connection
    
    conn, cursor = scraper.crypto_scraper.setup_db()
    
    assert mock_connect.called
    
    assert conn == mock_connection
    assert cursor == mock_cursor

@patch('scraper.crypto_scraper.setup_db')
def test_save_data_basic(mock_setup_db, sample_crypto_data):
    mock_cursor = MagicMock()
    mock_connection = MagicMock()
    mock_cursor.fetchone.return_value = (1,)
    mock_setup_db.return_value = (mock_connection, mock_cursor)
    
    scraper.crypto_scraper.save_data(sample_crypto_data)
    
    mock_connection.commit.assert_called_once()
    mock_connection.close.assert_called_once()

@patch('scraper.crypto_scraper.webdriver.Chrome')
def test_fetch_cryptos_simple(mock_chrome):
    mock_driver = MagicMock()
    mock_chrome.return_value = mock_driver
    
    mock_driver.find_elements.return_value = []
    
    result = scraper.crypto_scraper.fetch_cryptos()
    
    assert mock_chrome.called
    mock_driver.quit.assert_called_once()
    
    assert isinstance(result, list)

@patch('scraper.crypto_scraper.setup_db')
def test_get_latest_prices_simple(mock_setup_db):
    mock_cursor = MagicMock()
    mock_connection = MagicMock()
    mock_cursor.fetchall.return_value = [('Bitcoin', 'BTC', 60000.0, '2023-01-01')]
    mock_setup_db.return_value = (mock_connection, mock_cursor)
    
    result = scraper.crypto_scraper.get_latest_prices()
    
    assert mock_cursor.execute.called
    mock_connection.close.assert_called_once()
    
    assert len(result) == 1
    assert result[0][0] == 'Bitcoin'

@patch('scraper.crypto_scraper.setup_db')
def test_get_price_history_simple(mock_setup_db):
    mock_cursor = MagicMock()
    mock_connection = MagicMock()
    mock_cursor.fetchall.return_value = [(60000.0, '2023-01-01')]
    mock_setup_db.return_value = (mock_connection, mock_cursor)
    
    result = scraper.crypto_scraper.get_price_history('BTC', 1)
    
    mock_cursor.execute.assert_called_once()
    args = mock_cursor.execute.call_args[0]
    assert 'symbol = %s' in args[0]
    assert args[1][0] == 'BTC'
    
    assert len(result) == 1
    assert result[0][0] == 60000.0