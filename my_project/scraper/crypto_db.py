from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import sqlite3
from datetime import datetime
import time
import random

def setup_db():
    conn = sqlite3.connect('crypto_data.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS cryptocurrencies (id INTEGER PRIMARY KEY, name TEXT, symbol TEXT UNIQUE)''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS price_history (id INTEGER PRIMARY KEY, crypto_id INTEGER, price REAL, timestamp DATETIME, FOREIGN KEY (crypto_id) REFERENCES cryptocurrencies (id))''')
    conn.commit()
    return conn, cursor

def save_data(crypto_data):
    conn, cursor = setup_db()
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    for crypto in crypto_data:
        cursor.execute('INSERT OR IGNORE INTO cryptocurrencies (name, symbol) VALUES (?, ?)', (crypto['name'], crypto['symbol']))
        cursor.execute('SELECT id FROM cryptocurrencies WHERE symbol = ?', (crypto['symbol'],))
        crypto_id = cursor.fetchone()[0]
        cursor.execute('INSERT INTO price_history (crypto_id, price, timestamp) VALUES (?, ?, ?)', (crypto_id, crypto['price'], timestamp))
    
    conn.commit()
    conn.close()

def fetch_cryptos():
    options = Options()
    options.add_argument('--headless')
    driver = webdriver.Chrome(options=options)
    driver.get('https://coinmarketcap.com/')
    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, "table")))
    rows = driver.find_elements(By.CSS_SELECTOR, "table tbody tr")[:10]
    
    crypto_data = []
    for row in rows:
        try:
            name, symbol = row.find_element(By.CSS_SELECTOR, "td:nth-child(3)").text.split('\n')[:2]
            price = float(row.find_element(By.CSS_SELECTOR, "td:nth-child(4)").text.replace('$', '').replace(',', ''))
            crypto_data.append({'name': name, 'symbol': symbol, 'price': price})
        except:
            continue
    
    driver.quit()
    return crypto_data

def get_latest_prices():
    conn = sqlite3.connect('crypto_data.db')
    cursor = conn.cursor()
    cursor.execute('''SELECT c.name, c.symbol, p.price, p.timestamp FROM cryptocurrencies c JOIN (SELECT crypto_id, MAX(timestamp) AS max_time FROM price_history GROUP BY crypto_id) latest ON latest.crypto_id = c.id JOIN price_history p ON p.crypto_id = c.id AND p.timestamp = latest.max_time ORDER BY p.price DESC''')
    data = cursor.fetchall()
    conn.close()
    return data

def get_price_history(symbol, limit=10):
    conn = sqlite3.connect('crypto_data.db')
    cursor = conn.cursor()
    cursor.execute('''
        SELECT price, timestamp FROM price_history
        JOIN cryptocurrencies ON cryptocurrencies.id = price_history.crypto_id
        WHERE symbol = ? ORDER BY timestamp DESC LIMIT ?
    ''', (symbol, limit))
    data = cursor.fetchall()
    conn.close()
    return data

if __name__ == "__main__":
    time.sleep(random.uniform(1, 3))
    crypto_data = fetch_cryptos()
    
    if crypto_data:
        save_data(crypto_data)

        print("\nÚltimos precios de criptomonedas:")
        print("-" * 50)
        for i, crypto in enumerate(crypto_data, 1):
            print(f"{i}. {crypto['name']} ({crypto['symbol']}): ${crypto['price']:.2f}")

        # Mostrar historial de precios de BTC
        print("\nHistorial de precios de Bitcoin (BTC):")
        print("-" * 50)
        history = get_price_history("BTC", 5)
        for price, timestamp in history:
            print(f"{timestamp} - ${price:.2f}")
