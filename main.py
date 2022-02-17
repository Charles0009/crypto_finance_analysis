#from database import insert_into_existind_db, create_db
from apis.get_data_api_b import test_for_oldest_possible_data, get_all_tickers, get_all_usdt_tickers
#from scrapping.list_of_words_associated_to_crypto import insert_into_existind_db

# list_of_ticks_usdt = get_all_usdt_tickers()

# for name in list_of_ticks_usdt:
#     try:
#         oldest_value = test_for_oldest_possible_data(name)
#         print(name)
#         print(oldest_value)
#         create_db(name)
#         insert_into_existind_db(name, oldest_value)
#     except:
#         pass


return_list_of_pairs = []
list_of_tickers = get_all_tickers()
print(list_of_tickers)
for item in list_of_tickers:
        return_list_of_pairs.append(item['symbol'])

#insert_into_existind_db(return_list_of_pairs)