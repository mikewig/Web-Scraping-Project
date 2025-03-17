import requests
from bs4 import BeautifulSoup
import pandas as pd


def getCryptoData():
    url = "https://www.coingecko.com/es"
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "html.parser")
        rows = soup.find_all("tr", class_="coin-item")

        names = []
        prices = []
        changes = []
        market_caps = []

        for row in rows:
            try:
                name = row.find("div", class_="tw-text-gray-700 dark:tw-text-moon-100").text.strip()
                #symbol = row.find("div", class_="tw-block tw-inline tw-text-xs tw-leading-4 tw-text-gray-500").text.strip()
                price = row.find("span", class_="data-prev-price").text.strip()
                change = row.find("span", class_="data-price-btc").text.strip()
                market_cap = row.find("span", class_="data-prev-price").text.strip()

                names.append(name)
                prices.append(price)
                changes.append(change)
                market_caps.append(market_cap)
            except AttributeError:
                continue

        
        data = {
            "Nombre": names,
            #"Symbols": symbol,
            "Precio": prices,
            "Cambio 24h": changes,
            "Capitalización de mercado": market_caps
        }
        df = pd.DataFrame(data)
        return df
    else:
        return None