# ----------------------------------------------------------------------------------
# # Correlating Google with Bitcoin Metrics
# ----------------------------------------------------------------------------------


import pandas as pd 
import numpy as np
import time

from scipy.stats import spearmanr

print("BITCOIN DATA")

target_list = ['market-price', 'estimated-transaction-volume', 'estimated-transaction-volume-usd', 
               'trade-volume', 'n-unique-addresses', 'BTC-transact-vol-per-address', 
               'USD-transact-vol-per-address', 'exchange-transaction-ratio', 'isPriceIncrease',
               'priceVolatility']

bitcoin = pd.read_csv('./dataPrep/BITCOIN/blockchain_info_processed.csv')

print("GOOGLE DATA")

google = pd.read_csv('./dataPrep/GOOGLE/google_trends.csv')

google['EpochDate'] = google.Day.apply(lambda x: time.mktime(time.strptime(x + ' UTC', "%Y-%m-%d %Z")) ).astype("int64")

google['Bitcoin - Cash'] = google['Bitcoin'].pct_change(1)

google = google[['EpochDate', 'Bitcoin - Cash']]

print("COMBINE DATA")

combData = pd.merge(google, bitcoin, on='EpochDate', how = 'left')

print("CORRELATIONS")

def round_value(x, th=0.0001):
    if abs(x) >= th:
        return(np.round(x,4))
    else:
        return("<0.0001")

def determine_signficance(p, target_list):
    if p <= 0.01/len(target_list): return("*")
    return("")

def correlations(target_list, combData, term, shift=0):

    allData = combData.copy()

    if shift != 0:
        for target in target_list:
            allData[target] = allData[target].shift(shift)
    
    p1 = allData[allData.EpochDate.apply(lambda x: (x >= 1483228800) & (x < 1513382400) )]
    p2 = allData[allData.EpochDate.apply(lambda x: (x >= 1513382400) & (x < 1530230400) )]
    p3 = allData[allData.EpochDate.apply(lambda x: (x >= 1530230400) & (x < 1542240000) )]
    
    correl = pd.DataFrame(dict(
                Metric = target_list
        ))

    stage_list = ['allData', 'p1', 'p2', 'p3']

    for stage in stage_list:
        exec(f"{stage}_SR = []")
        exec(f"{stage}_PVALUE = []")
        exec(f"{stage}_isSig = []")

    for target in target_list:       

        for stage in stage_list:
            
            data = eval(f"{stage}.copy()")

            r, p = spearmanr(
                data[term], 
                data[target],
                nan_policy='omit'
                )
            sig = determine_signficance(p,target_list)
            
            exec(f"{stage}_SR.append(r)")
            exec(f"{stage}_PVALUE.append(p)")
            exec(f"{stage}_isSig.append(sig)")
    
    for stage in stage_list:

        exec(f"correl['{stage}_SR'] = {stage}_SR")
        exec(f"correl['{stage}_isSig'] = {stage}_isSig")
        exec(f"correl['{stage}_PVALUE'] = {stage}_PVALUE")

        correl[f'{stage}_SR'] = correl[f'{stage}_SR'].apply(lambda x: round_value(x))
        correl[f'{stage}_PVALUE'] = correl[f'{stage}_PVALUE'].apply(lambda x: round_value(x))

        exec(f"correl['{stage}_SR'] = correl['{stage}_SR'].astype(str) + correl['{stage}_isSig']")

        exec(f"del correl['{stage}_isSig']")

    return(correl)


for shift in [0,-1,-2]:
    print(
        shift, "\n",
        correlations(
            term = 'Bitcoin - Cash',
            target_list=target_list, 
            combData = combData,
            shift=shift).to_latex(index=False),
            "\n\n"
    )