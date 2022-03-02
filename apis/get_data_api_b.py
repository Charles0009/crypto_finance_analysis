import json
from binance import Client, ThreadedWebsocketManager, ThreadedDepthCacheManager
from defer import return_value
import pandas as pd
import datetime
import os


api_key = "WA57b7Xw7jhd5P1t78Z3gj6AuB8D9iSgbaZJEs16TjyJCfw2ds8mIUJdQDqmAVXG"
api_secret = "9m2mU7iWLWS2v0q2rgFzkdyGx3gSUIMi1n6Sx9ItBInWL1y7Cxl6Tf5A2AwTYzA7"
client = Client(api_key, api_secret)





def get_list_of_future_coins():
    futures_exchange_info = client.futures_exchange_info()  # request info on all futures symbols
    trading_pairs = [info['symbol'] for info in futures_exchange_info['symbols']]
    return trading_pairs

def get_exchange_infos():
    

    info = client.get_exchange_info()
    return info

def get_pd_daily_histo(pair, since):
        
    ##### get historical data

    historical = client.get_historical_klines(pair, Client.KLINE_INTERVAL_1DAY, since)
    hist_df = pd.DataFrame(historical)
    hist_df.columns = ['Open_Time', 'Open', 'High', 'Low', 'Close', 'Volume', 'Close_Time', 'Quote_Asset_Volume', 
                        'Number_of_Trades', 'TB_Base_Volume', 'TB_Quote_Volume', 'Ignore']

    hist_df = hist_df.drop(['Quote_Asset_Volume', 'TB_Base_Volume', 'TB_Quote_Volume','Ignore'], axis=1)

    hist_df['Open_Time'] = pd.to_datetime(hist_df['Open_Time']/1000, unit='s')
    hist_df['Close_Time'] = pd.to_datetime(hist_df['Close_Time']/1000, unit='s')

    numeric_columns = ['Open', 'High', 'Low', 'Close', 'Volume']

    hist_df[numeric_columns] = hist_df[numeric_columns].apply(pd.to_numeric, axis=1)

    return(hist_df)


def get_pd_daily_histo_between_dates(pair, since, end):
        
    ##### get historical data

    historical = client.get_historical_klines(pair, Client.KLINE_INTERVAL_1DAY, since, end)
    hist_df = pd.DataFrame(historical)

    hist_df.columns = ['Open_Time', 'Open', 'High', 'Low', 'Close', 'Volume', 'Close_Time', 'Quote_Asset_Volume', 
                        'Number_of_Trades', 'TB_Base_Volume', 'TB_Quote_Volume', 'Ignore']
    

    hist_df = hist_df.drop(['Quote_Asset_Volume', 'TB_Base_Volume', 'TB_Quote_Volume','Ignore'], axis=1)

    hist_df['epoch_time'] = hist_df['Open_Time']
    hist_df['epoch_time'] = hist_df['epoch_time'] / 1000

    hist_df['Open_Time'] = pd.to_datetime(hist_df['Open_Time']/1000, unit='s')
    hist_df['Close_Time'] = pd.to_datetime(hist_df['Close_Time']/1000, unit='s')

    numeric_columns = ['Open', 'High', 'Low', 'Close', 'Volume']

    hist_df[numeric_columns] = hist_df[numeric_columns].apply(pd.to_numeric, axis=1)

    hist_df['mean_daily_price'] = hist_df.loc[:, ['Open', 'Close']].mean(axis=1) 

    #print(hist_df)

    return(hist_df)

def get_pd_hourly_histo(pair, since):
        
    ##### get historical data

    historical = client.get_historical_klines(pair, Client.KLINE_INTERVAL_1HOUR, since)
    hist_df = pd.DataFrame(historical)
    hist_df.columns = ['Open_Time', 'Open', 'High', 'Low', 'Close', 'Volume', 'Close_Time', 'Quote_Asset_Volume', 
                        'Number_of_Trades', 'TB_Base_Volume', 'TB_Quote_Volume', 'Ignore']

    hist_df = hist_df.drop(['Quote_Asset_Volume', 'TB_Base_Volume', 'TB_Quote_Volume','Ignore'], axis=1)

    hist_df['Open_Time'] = pd.to_datetime(hist_df['Open_Time']/1000, unit='s')
    hist_df['Close_Time'] = pd.to_datetime(hist_df['Close_Time']/1000, unit='s')

    numeric_columns = ['Open', 'High', 'Low', 'Close', 'Volume']

    hist_df[numeric_columns] = hist_df[numeric_columns].apply(pd.to_numeric, axis=1)


    return(hist_df)


def test_for_oldest_possible_data(pair):

     ##### get historical data
    historical = client.get_historical_klines(pair, Client.KLINE_INTERVAL_1DAY, '01 Jan 2000')
    hist_df = pd.DataFrame(historical)
    hist_df.columns = ['Open_Time', 'Open', 'High', 'Low', 'Close', 'Volume', 'Close_Time', 'Quote_Asset_Volume', 
                        'Number_of_Trades', 'TB_Base_Volume', 'TB_Quote_Volume', 'Ignore']

    hist_df = hist_df.drop(['Quote_Asset_Volume', 'TB_Base_Volume', 'TB_Quote_Volume','Ignore'], axis=1)

    hist_df['Open_Time'] = pd.to_datetime(hist_df['Open_Time']/1000, unit='s')
    hist_df['Close_Time'] = pd.to_datetime(hist_df['Close_Time']/1000, unit='s')

    numeric_columns = ['Open', 'High', 'Low', 'Close', 'Volume']

    hist_df[numeric_columns] = hist_df[numeric_columns].apply(pd.to_numeric, axis=1)

    value_to_return = hist_df.iloc[0]['Open_Time']
    value_to_return = value_to_return.strftime("%d %b %Y") 
    value_to_return = str(value_to_return)

    return(value_to_return)

def get_all_tickers():
    prices = client.get_all_tickers()    
    return(prices)

def get_list_of_symbols():
    prices = client.get_all_tickers()   
    return_list = list()
    return_list_of_usdt_pairs = list()
    for item in prices:
        if 'USDT' in item['symbol']:
            return_list_of_usdt_pairs.append(item['symbol'])

    for i in return_list_of_usdt_pairs:
        item = str(i)
        return_list.append(item[:-4]) 
        
    return(return_list)

def change_pair_to_first_crypto_small_cap(name_crytpo, lenght_second_pair) :
    name_crytpo = name_crytpo[:-lenght_second_pair]
    #get to small caps
    name_crytpo.lower()
    return (name_crytpo)


def get_all_usdt_tickers():
    return_list_of_usdt_pairs = list()
    all = get_all_tickers()
    for item in all:
        if 'USDT' in item['symbol']:
            return_list_of_usdt_pairs.append(item['symbol'])

    return(return_list_of_usdt_pairs)

def get_list_of_crypto_names():
    # Opening JSON file
    chemin = os.getcwd()
    f = open(chemin+'/crypto_json_names.json')
    
    # returns JSON object as
    # a dictionary
    data = json.load(f)
    
    # Iterating through the json
    liste1 = get_list_of_symbols()
    new_liste = list()
    for element in liste1:
        try:
            new_liste.append(data[element])
            new_liste.append(element)

        except KeyError:
            pass
    [x.lower() for x in new_liste]

    new_liste = list(map(lambda x: x.lower(), new_liste))


    return(new_liste)

# start_text = pd.to_datetime(1583107200, unit='s')
# start_text = start_text.strftime("%d %b %Y") 
# end_text = pd.to_datetime(1646179200, unit='s')
# end_text = end_text.strftime("%d %b %Y") 

# list1 = get_pd_daily_histo_between_dates('BTCUSDT', start_text, end_text)

# list1.to_csv('blockchain_info_test_bin.csv')