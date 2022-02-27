
import os
import matplotlib.pyplot as plt
from turtle import left
from apis.get_data_api_b import get_list_of_coins, get_list_of_crypto_names, get_pd_daily_histo_between_dates
from BurnieYilmazRS19.dataPrep.REDDIT.main_extract import extract_full_reddit_token_frequency

import pandas as pd

#get token frequency 


# start = 1634251200
# end =   1644830527
# subreddit= 'CryptoMarkets'


name_for_file_pickle_reddit = extract_full_reddit_token_frequency(1634251200,1644830527, 'CryptoMarkets')



current_directory = str(os.getcwd())
path_for_pickle_file = current_directory+'/BurnieYilmazRS19/dataPrep/REDDIT/data/extracting/'+name_for_file_pickle_reddit+'.pkl'

reddit = pd.read_pickle(path_for_pickle_file)



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


# plt.subplot(2, 1, 1)
plt.plot(combined_df['Open_Time'], combined_df['Close'], color='blue')
plt.ylabel('price')
plt.twinx()
plt.bar(combined_df['Open_Time'], combined_df['nb_mentions'],color='green')
plt.ylabel('nb mentions reddit')


# plt.plot(combined_df['Open_Time'], combined_df['Close'])
# plt.bar(combined_df['Open_Time'],combined_df['Nb_mentions'])
plt.show()


