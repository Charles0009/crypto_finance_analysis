import numpy as np
import pandas_datareader as pdr
import datetime as dt
import pandas as pd
import matplotlib.pyplot as plt

from get_data_api_b import get_pd_histo


start = dt.datetime(2020, 9, 1)
date_in_string = start.strftime("%d %b %Y ") 

list_of_tickers = ['BTCUSDT', 'ETHUSDT', 'XTZUSDT', 'SOLUSDT' ]

data = pd.DataFrame()

for tick in list_of_tickers:
    dataiso = get_pd_histo(tick, date_in_string)
    dataiso = dataiso.set_index('Open_Time')
    dataiso = dataiso['Close']
    data[tick] = dataiso

portfolio = [.25, .15, .40, .20]

log_return  = np.sum(np.log(data/data.shift())*portfolio, axis=1)

# fig, ax = plt.subplots()
# log_return.hist(bins=50, ax=ax)
# plt.show()

return_daily = log_return.mean()
std_daily = log_return.std()

sharpe_ratio = log_return.mean()/log_return.std()

annualized_shape_ratio =  sharpe_ratio*364**.5



weight = np.random.random(4)
weight /= weight.sum()

log_return2 = np.sum(np.log(data/data.shift())*weight, axis=1)
sharpe_ratio2 = log_return2.mean()/log_return2.std()
asr2 = sharpe_ratio2*364**.5

print('portfolio')
print(portfolio)
print(annualized_shape_ratio)
print('randomly')
print(weight)
print(asr2)
