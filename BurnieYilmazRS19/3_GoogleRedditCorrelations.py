# ----------------------------------------------------------------------------------
# # Correlating Reddit with Google
# ----------------------------------------------------------------------------------


import pandas as pd 
import numpy as np
import time
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

print("Combine Datasets")

combData = pd.merge(reddit, google, on='EpochDate', how = 'left')

p1 = combData[combData.EpochDate.apply(lambda x: (x >= 1483228800) & (x < 1513382400) )]
p2 = combData[combData.EpochDate.apply(lambda x: (x >= 1513382400) & (x < 1530230400) )]
p3 = combData[combData.EpochDate.apply(lambda x: (x >= 1530230400) & (x < 1542240000) )]

print("CORRELATIONS")

print("Google - Reddit")

for i, data in zip(['combData', 'p1', 'p2', 'p3'], [combData, p1, p2, p3]):
    print(i)
    r, p = spearmanr(
                data['Bitcoin'], 
                data['no_submissions'],
                nan_policy='omit'
                )
    print("Correlation: ", r, "\n", "p-value: ", p)