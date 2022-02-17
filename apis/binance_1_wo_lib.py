from __future__ import print_function

from get_data_api_b import get_pd_histo
from binance import Client, ThreadedWebsocketManager, ThreadedDepthCacheManager
import pandas as pd
import mplfinance as mpf
import statsmodels.tsa.stattools as ts
from datetime import datetime
from numpy import cumsum, log, polyfit, sqrt, std, subtract
from numpy.random import randn
import numpy as np


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

hist_df = get_pd_histo('BTCUSDT', '17 Aug 2017')

# print(hist_df.shape)
# print(hist_df['Close'].describe())
#print(hist_df['Close_Time'])
print(hist_df['Open_Time'].dt.month)


#print(hist_df.columns)
# print(hist_df.info())

#### visualize the data

# mpf.plot(hist_df.set_index('Close Time').tail(1020), 
#         type='candle', style='charles', 
#         volume=True, 
#         title='ETHBTC Last 1020 Days', 
#         mav=(10,20,30))


# Augmented Dickey-Fuller test
# print(ts.adfuller(hist_df['Close'],1))



# test for linearity 

# def hurst(ts, maxlag = 10):
#     """Returns the Hurst Exponent of the time series vector ts"""
#     # Create the range of lag values
#     lags = range(2, maxlag)
#     # Calculate the array of the variances of the lagged differences
#     tau = [np.std(np.subtract(ts[lag:], ts[:-lag])) for lag in lags]
#     # calculate the slope of the log plot -> the Hurst Exponent
#     reg = np.polyfit(np.log(lags), np.log(tau), 1)
#     # Return the Hurst exponent from the polyfit output
#     return reg[0]

# # Create a Gometric Brownian Motion, Mean-Reverting and Trending Series
# gbm = log(cumsum(randn(100000))+1000)
# mr = log(randn(100000)+1000)
# tr = log(cumsum(randn(100000)+1)+1000)

# print("Hurst(GBM): %s" % hurst(gbm))
# print("Hurst(MR): %s" % hurst(mr))
# print("Hurst(TR): %s" % hurst(tr))
# print("Hurst(BTC): %s" % hurst(hist_df['Close']))
