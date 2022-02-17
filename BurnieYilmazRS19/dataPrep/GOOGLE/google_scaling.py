# ----------------------------------------------------------------------------------
# # Scaling Google Data to be of Same Units
# ----------------------------------------------------------------------------------

# Source: https://trends.google.com

import pandas as pd
import numpy as np

from scipy.stats import mode, hmean
from scipy.stats.mstats import gmean
from functools import reduce

def normalise_and_join(data, prev, term='Bitcoin'):
    
    earlier = prev[prev['Day'] >= np.min(data['Day'])]
    earlier.reset_index(inplace = True)
    
    latter = data[data.Day <= np.max(prev.Day)]
    latter.reset_index(inplace = True)
    
    frame = pd.DataFrame({'Day': latter.Day,
                 'earlier': earlier[term + ': (Worldwide)'],
                 'latter': latter[term]})
    
    frame = frame[(frame.T != 0).all()]
        
    mult = frame['latter']/frame['earlier']
    
    earlier_convert = prev[prev.Day < np.min(data.Day)].copy()
    
    earlier_convert.columns = ['Day', term]
    
    earlier_convert[term] = earlier_convert[term] * hmean(mult)
    
    return(pd.concat([
        earlier_convert,
        data
    ]
    ))



def google_aggregator(datatype):

    word = 'Bitcoin' if datatype == 'topic' else datatype

    dataDict = dict(
        A1 = None,
        A2 = None,
        A3 = None,
        A4 = None,
        A5 = None
    )

    for var in range(1,6):
        dataDict[f"A{var}"] = pd.read_csv(f'./data/{datatype}/A{var}.csv', skiprows=1)
        #Replacing <1 with 0:
        dataDict[f"A{var}"][f"{word}: (Worldwide)"] = dataDict[f"A{var}"][f"{word}: (Worldwide)"].apply(lambda x: 0 if x == "<1" else float(x))

    search = dataDict["A5"][['Day']]

    search[word] = dataDict["A5"].iloc[:,1]/dataDict["A5"].tail(1).iloc[0,1]*100    
    
    search_data2 = reduce(
        lambda latter, former: normalise_and_join(latter, former, term=word),
      [search, dataDict["A4"], dataDict["A3"], dataDict["A2"], dataDict["A1"]]
      )

    return(search_data2)

google_aggregator('topic').to_csv('google_trends.csv', index=False)


A4 = pd.read_csv('./data/topic/A4.csv', skiprows=1)
A5 = pd.read_csv('./data/topic/A5.csv', skiprows=1)

print("Which Averaging Approach?")

earlier = A4[A4.Day >= np.min(A5['Day'])]
earlier.reset_index(inplace = True)

latter = A5[A5.Day <= np.max(A4['Day'])]
latter.reset_index(inplace = True)

frame = pd.DataFrame({'Day': latter.Day,
                 'earlier': earlier['Bitcoin: (Worldwide)'],
                 'latter': latter['Bitcoin: (Worldwide)']})

frame = frame[(frame.T != 0).all()]

mult = frame['latter']/frame['earlier']

print("mean")
per_diff = frame['earlier'] * np.mean(mult) / frame['latter'] - 1 
print(  "mean - " + str(np.mean(per_diff)))
print(  "max - " + str(np.max(per_diff)))

print("\n mode")
per_diff = frame['earlier'] * mode(mult).mode[0] / frame['latter'] - 1
print(  "mean - " + str(np.mean(per_diff)))
print(  "max - " + str(np.max(per_diff)))

print("\n median")
per_diff = frame['earlier'] * np.median(mult) / frame['latter'] - 1
print(  "mean - " + str(np.mean(per_diff)))
print(  "max - " + str(np.max(per_diff)))

print("\n geo mean")
per_diff = frame['earlier'] * gmean(mult) / frame['latter'] - 1
print(  "mean - " + str(np.mean(per_diff)))
print(  "max - " + str(np.max(per_diff)))

print("\n harmonic mean")
per_diff = frame['earlier'] * hmean(mult) / frame['latter'] - 1
print(  "mean - " + str(np.mean(per_diff)))
print(  "max - " + str(np.max(per_diff)))

print("harmonic mean had lowest average error")