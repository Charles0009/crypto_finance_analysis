from binance import Client, ThreadedWebsocketManager, ThreadedDepthCacheManager
import pandas as pd
import mplfinance as mpf



api_key = "WA57b7Xw7jhd5P1t78Z3gj6AuB8D9iSgbaZJEs16TjyJCfw2ds8mIUJdQDqmAVXG"
api_secret = "9m2mU7iWLWS2v0q2rgFzkdyGx3gSUIMi1n6Sx9ItBInWL1y7Cxl6Tf5A2AwTYzA7"
client = Client(api_key, api_secret)

###### get ticker for current prices 

# tickers = client.get_all_tickers()
# ticker_df = pd.DataFrame(tickers)
# ticker_df.set_index('symbol', inplace=True)
# print(ticker_df.head())




##### get market depth for particular pair

# depth = client.get_order_book(symbol='BTCUSDT')
# depth_df = pd.DataFrame(depth['bids'])
# depth_df.columns = ['Price', 'Volume']
# print(depth_df.head)




##### get historical data

historical = client.get_historical_klines('BTCUSDT', Client.KLINE_INTERVAL_1DAY, '1 Jan 2011')
hist_df = pd.DataFrame(historical)
hist_df.columns = ['Open Time', 'Open', 'High', 'Low', 'Close', 'Volume', 'Close Time', 'Quote Asset Volume', 
                    'Number of Trades', 'TB Base Volume', 'TB Quote Volume', 'Ignore']

hist_df['Open Time'] = pd.to_datetime(hist_df['Open Time']/1000, unit='s')
hist_df['Close Time'] = pd.to_datetime(hist_df['Close Time']/1000, unit='s')

numeric_columns = ['Open', 'High', 'Low', 'Close', 'Volume', 'Quote Asset Volume', 'TB Base Volume', 'TB Quote Volume']

hist_df[numeric_columns] = hist_df[numeric_columns].apply(pd.to_numeric, axis=1)

print(hist_df.shape)

# print(hist_df.describe())
# print(hist_df.info())

#### visualize the data


mpf.plot(hist_df.set_index('Close Time').tail(1020), 
        type='candle', style='charles', 
        volume=True, 
        title='ETHBTC Last 1020 Days', 
        mav=(10,20,30))




