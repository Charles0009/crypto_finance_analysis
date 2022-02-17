# ------------------------------------------------------------------------------------------
# -- ADF Testing
# ---- Follows Stock and Watson (2012)
# ------------------------------------------------------------------------------------------


import pandas as pd 
import numpy as np
import time
from statsmodels.tsa.stattools import adfuller
from scipy.stats.mstats import gmean, hmean
import statsmodels

from scipy.stats import spearmanr

print("Import Google Data")

google = pd.read_csv('./dataPrep/GOOGLE/google_trends.csv')

google['EpochDate'] = google.Day.apply(lambda x: time.mktime(time.strptime(x + ' UTC', "%Y-%m-%d %Z")) ).astype("int64")

google['Bitcoin'] = google['Bitcoin'].pct_change(1)

del google['Day']

print("Import Reddit Data")

reddit = pd.read_pickle('./dataPrep/REDDIT/data/processing/tokenFreq/dailyTokenFreq_041218.pkl')
reddit.rename(index=str, columns={"day_time_stamp": "EpochDate"}, inplace=True)

reddit = reddit[['EpochDate'] + ['no_submissions'] ]

reddit["no_submissions"] = reddit['no_submissions'].pct_change(1)

print("Import Bitcoin Metrics")

target_list = ['market-price', 'estimated-transaction-volume', 'estimated-transaction-volume-usd', 
               'trade-volume', 'n-unique-addresses', 'BTC-transact-vol-per-address', 
               'USD-transact-vol-per-address', 'exchange-transaction-ratio', 'isPriceIncrease',
               'priceVolatility']

bitcoin = pd.read_csv('./dataPrep/BITCOIN/blockchain_info_processed.csv')


print("Combine Datasets")

combData = pd.merge(pd.merge(reddit, google, on='EpochDate', how = 'left'), bitcoin, on='EpochDate', how = 'left')

p1 = combData[combData.EpochDate.apply(lambda x: (x >= 1483228800) & (x < 1513382400) )]
p2 = combData[combData.EpochDate.apply(lambda x: (x >= 1513382400) & (x < 1530230400) )]
p3 = combData[combData.EpochDate.apply(lambda x: (x >= 1530230400) & (x < 1542240000) )]

print("ADF Tests")

print("Reddit (no_submissions) and Google (Bitcoin)")

for col in ['no_submissions', 'Bitcoin']:
    print("\n\n",col)
    for i,data in zip(['p1', 'p2', 'p3'], [p1, p2, p3]):
        print(i)
        print(
        adfuller(data[col][1::].tolist(), 
         regression = 'c',   #including constant
         autolag = 'AIC'
        )[1] 
        )

print("Bitcoin Metrics")

for col in target_list:
    print("\n\n",col)
    for i,data in zip(['p1', 'p2', 'p3'], [p1, p2, p3]):
        print(i)
        print(
        adfuller(data[col].tolist(), 
         regression = 'c',   #including constant
         autolag = 'AIC'
        )[1] 
        )


