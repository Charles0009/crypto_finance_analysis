

from apis.get_data_api_b import get_list_of_coins, get_list_of_crypto_names

import pandas as pd


reddit = pd.read_pickle('BurnieYilmazRS19/dataPrep/REDDIT/data/processing/tokenFreq/CryptoMarkets_2021-10-15_2022-02-14.pkl')

col_list_names = get_list_of_crypto_names()
col_list_symbol = get_list_of_coins()



col_list_symbol = list(map(lambda x: x.lower(), col_list_symbol))



liste_totale = col_list_names + col_list_symbol
liste_totale.append('day_time_stamp')
liste_totale.append('no_submissions')
reddit_sub = reddit['eth']

df2 = reddit[reddit.columns[reddit.columns.isin(liste_totale)]]

df2.to_csv('export/sub_for_crypto_names.csv')

print(df2)