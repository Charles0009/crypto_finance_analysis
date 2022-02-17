from binance import Client, ThreadedWebsocketManager, ThreadedDepthCacheManager
import pandas as pd
import datetime



api_key = "WA57b7Xw7jhd5P1t78Z3gj6AuB8D9iSgbaZJEs16TjyJCfw2ds8mIUJdQDqmAVXG"
api_secret = "9m2mU7iWLWS2v0q2rgFzkdyGx3gSUIMi1n6Sx9ItBInWL1y7Cxl6Tf5A2AwTYzA7"
client = Client(api_key, api_secret)




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

def get_all_usdt_tickers():
    return_list_of_usdt_pairs = list()
    all = get_all_tickers()
    for item in all:
        if 'USDT' in item['symbol']:
            return_list_of_usdt_pairs.append(item['symbol'])

    return(return_list_of_usdt_pairs)


