
import pandas as pd
import numpy as np
import mplfinance 
from mplfinance.original_flavor import candlestick_ohlc
import yfinance
import matplotlib.dates as mpl_dates
import matplotlib.pyplot as plt
import os
import sys

# Insert the path of modules folder
sys.path.insert(0, str(os.getcwd())+'/apis/')

from get_data_api_b import get_pd_daily_histo_between_dates



df = get_pd_daily_histo_between_dates('BTCUSDT', "2021-03-15", "2021-07-15")
df.rename(columns = {'Open_Time':'Date'}, inplace = True)

data = df

print(data.head())

#data = pd.DataFrame.from_csv('tmpData.txt')
data['swings'] = np.nan

pivot = data['Open'].iloc[0]
print(pivot)
last_pivot_id = 0
up_down = 0

diff = .3

for i in range(0, len(data)):

    row = data.iloc[i]
    print("row")
    print(row)
    # We don't have a trend yet
    if up_down == 0:
        if row['Low'] < pivot - diff:
            data.loc[i, 'swings'] = row['Low']  - pivot
            pivot, last_pivot_id = row['Low'] , i
            up_down = -1
        elif row['High'] > pivot + diff:
            data.loc[i, 'swings'] = row['High'] - pivot
            pivot, last_pivot_id = row['High'], i
            up_down = 1

    # Current trend is up
    elif up_down == 1:
        # If got higher than last pivot, update the swing
        if row['High'] > pivot:
            # Remove the last pivot, as it wasn't a real one
            data.loc[i, 'swings'] = data.loc[last_pivot_id, 'swings'] + (row['High'] - data.loc[last_pivot_id, 'High'])
            data.loc[last_pivot_id, 'swings'] = np.nan
            pivot, last_pivot_id = row['High'], i
        elif row['Low'] < pivot - diff:
            data.loc[i, 'swings'] = row['Low'] - pivot
            pivot, last_pivot_id = row['Low'], i
            # Change the trend indicator
            up_down = -1

    # Current trend is down
    elif up_down == -1:
            # If got lower than last pivot, update the swing
        if row['Low'] < pivot:
            # Remove the last pivot, as it wasn't a real one
            data.loc[i, 'swings'] = data.loc[last_pivot_id, 'swings'] + (row['Low'] - data.loc[last_pivot_id, 'Low'])
            data.loc[last_pivot_id, 'swings'] = np.nan
            pivot, last_pivot_id = row['Low'], i
        elif row['High'] > pivot - diff:
            data.loc[i, 'swings'] = row['High']  - pivot
            pivot, last_pivot_id = row['High'] , i
            # Change the trend indicator
            up_down = 1

print (data.head(30))