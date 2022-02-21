
import matplotlib.pyplot as plt
from turtle import left
from apis.get_data_api_b import get_list_of_coins, get_list_of_crypto_names, get_pd_daily_histo_between_dates

import pandas as pd


reddit = pd.read_pickle('BurnieYilmazRS19/dataPrep/REDDIT/data/processing/tokenFreq/CryptoMarkets_2021-10-15_2022-02-14.pkl')

col_list_names = get_list_of_crypto_names()
col_list_symbol = get_list_of_coins()



col_list_symbol = list(map(lambda x: x.lower(), col_list_symbol))





liste_totale = col_list_names + col_list_symbol
liste_totale.append('day_time_stamp')
liste_totale.append('no_submissions')
#reddit_sub = reddit['eth']





df2 = reddit[reddit.columns[reddit.columns.isin(liste_totale)]]

df_dates = df2['day_time_stamp']
eth_mentions = df2['eth'] + df2['ethereum']

df_dates = df_dates.to_frame()
eth_mentions = eth_mentions.to_frame()

final_df = df_dates.join(eth_mentions)

#print(final_df)

final_df['day_time_stamp'] = pd.to_datetime(final_df['day_time_stamp'], unit='s')


final_df['day_time_stamp'] = pd.to_datetime(final_df['day_time_stamp']).dt.date
final_df['day_time_stamp'] = pd.DatetimeIndex(final_df['day_time_stamp']) + pd.DateOffset(1)
final_df.columns = ['Open_Time', 'nb_mentions']

pd_eth = get_pd_daily_histo_between_dates('ETHUSDT', '15 Oct 2021', '14 Feb 2022')

combined_df = pd.merge(final_df, pd_eth, on=['Open_Time'])


