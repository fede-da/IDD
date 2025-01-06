import pandas as pd
import numpy as np
import json

# Funzione per convertire i valori di MarketCap in float
def clean_market_cap(value):
    if isinstance(value, str):
        value = value.replace('$', '').replace('T', 'e12').replace('B', 'e9').replace('M', 'e6')
        try:
            return float(eval(value))
        except:
            return np.nan
    return value

# Caricamento e unificazione dei dati da diversi file JSON
data = []

# companiesmarketcap.json
with open('../../../data/marketcap', 'r') as file:
    json_data = json.load(file)
    for item in json_data:
        data.append({'CompanyName': item['name'], 'MarketCap': clean_market_cap(item['marketcap']), 'Revenue': np.nan})