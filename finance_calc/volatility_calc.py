import numpy as np
import pandas_datareader as pdr
import datetime as dt
import pandas as pd
import matplotlib.pyplot as plt

from get_data_api_b import get_pd_daily_histo


start = dt.datetime(2020, 9, 1)
symbol = 'BTCUSDT'

date_in_string = start.strftime("%d %b %Y ") 
data = get_pd_daily_histo(symbol, date_in_string)
data = data.set_index('Open_Time')

high_low = data['High'] - data['Low']
high_cp = np.abs(data['High'] - data['Close'].shift())
low_cp = np.abs(data['Low'] - data['Close'].shift())

df = pd.concat([high_low, high_cp, low_cp], axis=1)
true_range = np.max(df, axis=1)
average_true_range = true_range.rolling(14).mean()

fig, ax = plt.subplots()
average_true_range.plot(ax=ax)
ax2 = data['Close'].plot(ax=ax, secondary_y=True, alpha=.3)
ax.set_ylabel("ATR")
ax2.set_ylabel("Price")

plt.show()