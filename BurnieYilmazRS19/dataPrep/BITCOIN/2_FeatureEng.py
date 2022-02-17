import pandas as pd 
import numpy as np

print("Import Price Data")

target_list = ['market-price', 'estimated-transaction-volume', 'estimated-transaction-volume-usd', 
               'trade-volume', 'n-unique-addresses']

priceData = pd.read_csv('blockchain_info_051218.csv')

del priceData['my-wallet-n-users']

print("NEW TARGETS - BEFORE PCT CHANGE")

priceData['BTC-transact-vol-per-address'] = priceData['estimated-transaction-volume']/priceData['n-unique-addresses']
priceData['USD-transact-vol-per-address'] = priceData['estimated-transaction-volume-usd']/priceData['n-unique-addresses']
priceData['exchange-transaction-ratio'] = priceData['trade-volume']/priceData['estimated-transaction-volume-usd']

target_list.append('BTC-transact-vol-per-address')
target_list.append('USD-transact-vol-per-address')
target_list.append('exchange-transaction-ratio')

for target in target_list:
    priceData[target] = priceData[target].pct_change(1) 

print("NEW TARGETS - AFTER PCT CHANGE")

priceData['isPriceIncrease'] = (priceData['market-price'] > 0).astype(int)
priceData['priceVolatility'] = abs(priceData['market-price'])

priceData['priceVolatility'] = priceData['priceVolatility'].pct_change(1)


priceData.to_csv('blockchain_info_processed.csv')