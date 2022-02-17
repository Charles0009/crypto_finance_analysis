import talib as ta
import matplotlib.pyplot as plt
from get_data_api_b import test_for_oldest_possible_data, get_pd_daily_histo


plt.style.use('bmh')

name = "ETHUSDT"

oldest_value = test_for_oldest_possible_data(name)
df = get_pd_daily_histo(name, oldest_value)

close = df['Close']


output = ta.SMA(df['Close'])

df['Simple_MA'] = ta.SMA(df['Close'],100)
df['EMA'] = ta.EMA(df['Close'], timeperiod = 100)



df['momentum'] = ta.MOM(df['Close'], timeperiod=5)


# upper, middle, lower = ta.BBANDS(close, matype=MA_Type.T3)

df.plot(x="Close_Time", y=['Close', 'EMA', 'momentum'])

plt.show()