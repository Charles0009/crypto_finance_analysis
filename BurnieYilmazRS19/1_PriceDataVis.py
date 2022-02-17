# ----------------------------------------------------------------------------------
# # Visualising the Bitcoin Price Series
# ----------------------------------------------------------------------------------


import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.dates import date2num
import time
import matplotlib.dates as mdate
import datetime


def price_mark(data, start,end, ismax):

    #on prends le data entre start et max 
    subsetData = data[data.EpochDate.apply(lambda x: (x >= start) & (x <= end)) ]
    # on récupère le prix max sur la période
    price = max(subsetData['market-price']) if ismax else min(subsetData['market-price'])
    #

    # print(subsetData.nlargest(2, columns=['market-price']))
    # print(subsetData['market-price'])

    mark = subsetData.EpochDate[subsetData['market-price'].idxmax()] if ismax else subsetData.EpochDate[subsetData['market-price'].idxmin()]

    return(price,mark)

def epoch_to_date(epoch): return(time.strftime('%Y-%m-%d', time.gmtime(epoch)))



priceData = pd.read_csv('/mnt/c/Users/charl/Desktop/finance_perso/BurnieYilmazRS19/dataPrep/BITCOIN/blockchain_info_processed.csv')[['EpochDate', 'market-price']]

print("Descriptive Price Stats")

price_changes = priceData['market-price'].pct_change()[priceData.EpochDate.apply(lambda x: (x >= 1483228800) & (x <= 1543795200)) ]

print("Median change: ", price_changes.median()*100)

print(
    "Max change: ", price_changes.max()*100,
    "at Date: ", epoch_to_date(priceData[priceData['market-price'].pct_change() == price_changes.max()].EpochDate.tolist()[0])
    )

print(
    "Min change: ", price_changes.min()*100,
    "at Date: ", epoch_to_date(priceData[priceData['market-price'].pct_change() == price_changes.min()].EpochDate.tolist()[0])
    )


priceData = priceData[priceData.EpochDate.apply(lambda x: (x >= 1483228800) & (x <= 1543795200)) ]

#priceData['date'] = time.strftime("%d %b %Y", time.localtime((priceData['EpochDate'])))




start_price, start_mark = price_mark(priceData, 1483228800, 1483228800, ismax=True)

max_price, max_mark = price_mark(priceData, 1483228800, 1543795200, ismax=True)

pre_nov_low_price, pre_nov_low_mark = price_mark(priceData, 1514764800, 1541030400, ismax=False)

endData = priceData[priceData.EpochDate >= 1541030400]

epochtime = 1541030400

datetime2 = time.strftime("%d %b %Y", time.localtime(epochtime))

datetime = datetime.datetime.fromtimestamp(epochtime)
print('la date ; ' ,datetime2)

#low_surp_mark = endData[endData['market-price'] < pre_nov_low_price].EpochDate.tolist()[0]

end_price, end_mark = price_mark(priceData, 1543795200, 1543795200, ismax=True)

print("Key Figures")

print("START AT:", epoch_to_date(start_mark), "PRICE: ", start_price)
print("PEAK AT:",  epoch_to_date(max_mark), "PRICE: ", max_price)
print("PRENOV LOW:", epoch_to_date(pre_nov_low_mark), "PRENOV LOW PRICE: ", pre_nov_low_price)
#print("STABILITY ENDS:", epoch_to_date(low_surp_mark))
print("END AT:", end_mark, "END PRICE:", end_price)



print("Visualising data")

_, ax = plt.subplots()
ax.xaxis.set_major_formatter(mdate.DateFormatter("%b-%y"))
ax.xaxis.set_major_locator( mdate.MonthLocator())


plt.plot_date(priceData['EpochDate'], priceData['market-price'], linestyle = '-', marker='', color = 'k')

plt.xlim("01 Jan 2017", "03 Dec 2018")

plt.axvline(x=mdate.epoch2num(max_mark), color="black", linestyle = '--')
plt.axvline(x=mdate.epoch2num(pre_nov_low_mark), color="black", linestyle = '--')
#plt.axvline(x=mdate.epoch2num(low_surp_mark), color="black", linestyle = '--')

plt.text(x=mdate.epoch2num(1493596800),y=15000,s="Stage 1",fontsize=12)
plt.text(x=mdate.epoch2num(1518652800),y=15000,s="Stage 2",fontsize=12)
plt.text(x=mdate.epoch2num(1533081600),y=15000,s="Stage 3",fontsize=12)

plt.ylabel("US Dollar bitcoin price")
plt.xlabel("")
plt.xticks(rotation=45)
plt.tight_layout()
# plt.show()
plt.savefig('./visuals/BitcoinPriceSeries22.jpeg')

print("Examining Period 3")

max_price, max_mark = price_mark(priceData, 1530230400, 1542153600, ismax=True)
min_price, min_mark = price_mark(priceData, 1530230400, 1542153600, ismax=False)

p3 = priceData[priceData.EpochDate.apply(lambda x: (x >= 1530230400) & (x < 1542240000))]

print("MIN: ", min_price, " on ", epoch_to_date(min_mark))
print("MEDIAN: ", p3['market-price'].median())
print("MAX: ", max_price, " on ", epoch_to_date(max_mark))




