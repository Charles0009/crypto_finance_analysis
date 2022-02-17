import datetime as dt
import pandas as pd
import numpy as np
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


# ## theory
# def roll_dice():
#     return np.sum(np.random.randint(1, 7, 2))
# def monte_carlo_simulation(runs=1000):
#     results = np.zeros(2)
#     for _ in range(runs):
#         if roll_dice() == 7:
#             results[0] += 1
#         else:
#             results[1] += 1
#     return results
# results = np.zeros(1000)
# for i in range(1000):
#     results[i] = monte_carlo_simulation()[0]


## applied to data 
log_returns = np.log(data/data.shift())
weight = np.random.random(4)
weight /= weight.sum()
exp_rtn = np.sum(log_returns.mean()*weight)*364
exp_vol = np.sqrt(np.dot(weight.T, np.dot(log_returns.cov()*364, weight)))
sharpe_ratio = exp_rtn / exp_vol
print(weight)
print(sharpe_ratio)

n = 5000

weights = np.zeros((n, 4))
exp_rtns = np.zeros(n)
exp_vols = np.zeros(n)
sharpe_ratios = np.zeros(n)

for i in range(n):
    weight = np.random.random(4)
    weight /= weight.sum()
    weights[i] = weight
    
    exp_rtns[i] = np.sum(log_returns.mean()*weight)*364
    exp_vols[i] = np.sqrt(np.dot(weight.T, np.dot(log_returns.cov()*364, weight)))
    sharpe_ratios[i] = exp_rtns[i] / exp_vols[i]

print(sharpe_ratios.max())
print(weights[sharpe_ratios.argmax()])

fig, ax = plt.subplots()
ax.scatter(exp_vols, exp_rtns, c=sharpe_ratios)
ax.scatter(exp_vols[sharpe_ratios.argmax()], exp_rtns[sharpe_ratios.argmax()], c='r')
ax.set_xlabel('Expected Volatility')
ax.set_ylabel('Expected Return')
plt.show()
