#from database import insert_into_existind_db, create_db
import json
from apis.get_data_api_b import get_pd_daily_histo, test_for_oldest_possible_data, get_all_tickers, get_all_usdt_tickers, get_exchange_infos, get_list_of_future_coins, get_list_of_coins, get_list_of_crypto_names
#from scrapping.list_of_words_associated_to_crypto import insert_into_existind_db

#list_of_ticks_usdt = get_all_usdt_tickers()




# for name in list_of_ticks_usdt:
#     try:
#         oldest_value = test_for_oldest_possible_data(name)
#         print(name)
#         print(oldest_value)
#         create_db(name)
#         insert_into_existind_db(name, oldest_value)
#     except:
#         pass



##############################################################################

#get all data for pair 
# pair = 'BTCUSDT'

# # return_btc_all_time = []

# oldest_btc_value = test_for_oldest_possible_data(pair)

# print(oldest_btc_value)

# list_btc_usdt = get_pd_daily_histo(pair, oldest_btc_value)

# list_btc_usdt.to_csv('export/btc_all_time_daily.csv')
# print(list_btc_usdt)


##############################################################################
# # get list of all tickers 
# return_list_of_pairs = []
# list_of_tickers = get_all_tickers()
# print(list_of_tickers)
# for item in list_of_tickers:
#         return_list_of_pairs.append(item['symbol'])


 
new_liste = get_list_of_crypto_names()

print(new_liste)

list = get_all_tickers()

#insert_into_existind_db(return_list_of_pairs)