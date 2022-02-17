# ----------------------------------------------------------------------------------
# # Visualising the Google Search Series
# ----------------------------------------------------------------------------------


import importlib
import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.dates import date2num
import matplotlib.dates as mdate
import time
import datetime


print("Prepare Data")

#google = pd.read_csv('/mnt/c/Users/charl/Desktop/finance_perso/BurnieYilmazRS19/dataPrep/GOOGLE/google_trends.csv')

reddit = pd.read_pickle('/mnt/c/Users/charl/Desktop/finance_perso/BurnieYilmazRS19/dataPrep/REDDIT/data/processing/tokenFreq/dailyTokenFreq_041218.pkl')[['day_time_stamp', 'no_submissions']]

reddit['no_submissions'] = reddit['no_submissions'] / reddit['no_submissions'].tail(1).tolist()[0] * 100

# reddit['date'] = reddit['day_time_stamp']

reddit['date'] = pd.to_datetime(reddit['day_time_stamp'], unit = 's')

print(reddit.head())

#google['EpochDate'] = google.Day.apply(lambda x: time.mktime(time.strptime(x + ' UTC', "%Y-%m-%d %Z")) ).astype("int64")
#google['date'] = google['EpochDate']

print("Plot Data")

# _, ax = plt.subplots()
# ax.xaxis.set_major_formatter(mdate.DateFormatter("%b-%y"))
# ax.xaxis.set_major_locator( mdate.MonthLocator())

plt.axhline(y=100, linestyle = '-', color='gray')

marker=''

plt.plot_date(reddit['date'], reddit['no_submissions'], linestyle = '-' , color = 'darkred', label='Reddit')

#plt.plot_date(google['date'], google['Bitcoin'], linestyle = '-.', color = 'blue', label='Google')

#plt.xlim(1640623150, 1640823600)

# plt.axvline(x="16 Dec 2017", linestyle = '--', color='grey')
# plt.axvline(x="29 June 2018", linestyle = '--', color='grey')
# plt.axvline(x="15 Nov 2018", linestyle = '--', color='grey')

# plt.ylabel("")
# plt.xlabel("")

plt.show()
#plt.savefig('./visuals/GoogleReddit.jpeg')