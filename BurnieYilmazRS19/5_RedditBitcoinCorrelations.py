# ----------------------------------------------------------------------------------
# # Correlating Reddit with Bitcoin Metrics
# ----------------------------------------------------------------------------------
import os
import sys
working_dir = str(os.getcwd())
# Insert the path of modules folder
sys.path.insert(0, working_dir+'/BurnieYilmazRS19/dataPrep/BITCOIN/')
sys.path.insert(0, working_dir+'/BurnieYilmazRS19/dataPrep/REDDIT/')

from FeatureEng import get_crypto_data_treated
from main_extract import extract_full_reddit_token_frequency
from click import command
import pandas as pd
import numpy as np
import time
from scipy.stats import spearmanr
from decimal import Decimal




def get_reddit_crypto_corre(epoch_start, epoch_end, pair, subreddit):

    # print("COIN DATA")
    target_list = ['mean_daily_price', 'Volume',
                   'Number_of_Trades', 'isPriceIncrease', 'priceVolatility']
    # coin = pd.read_csv('./dataPrep/BITCOIN/blockchain_info_processed.csv')
    coin = get_crypto_data_treated(epoch_start, epoch_end, pair)
    print("REDDIT DATA")
    filepath = extract_full_reddit_token_frequency(
        epoch_start, epoch_end, subreddit)
    reddit = pd.read_pickle(filepath)
    # print(reddit.head())
    # reddit = pd.read_pickle( working_dir+'/BurnieYilmazRS19/dataPrep/REDDIT/data/processing/tokenFreq/CryptoMarkets_2021-10-15_2022-02-14.pkl')
    reddit.rename(index=str, columns={
                  "day_time_stamp": "EpochDate"}, inplace=True)
    coin.rename(index=str, columns={"epoch_time": "EpochDate"}, inplace=True)
    reddit = reddit[['EpochDate', 'no_submissions']]
    reddit['no_submissions'] = reddit['no_submissions'].pct_change(1)
    print("COMBINE DATA")
    reddit['EpochDate'] = round(reddit['EpochDate']/100000)
    coin['EpochDate'] = round(coin['EpochDate']/100000)
    combData = pd.merge(reddit, coin, on='EpochDate', how='left')

    #combData.to_csv(working_dir + '/combdata.csv')
    #combData = pd.read_csv(working_dir + '/combdata.csv')

    print("CORRELATIONS")

    def round_value(x, th=0.0001):
        if abs(x) >= th:
            return(np.round(x, 4))
        else:
            return("<0.0001")

    def determine_signficance(p, target_list):
        if p <= 0.01/len(target_list):
            return("*")
        return("")

    def correlations(target_list, combData, term, shift=0):

        allData = combData.copy()

        # if shift != 0:
        #     for target in target_list:
        #         allData[target] = allData[target].shift(shift)
        # p1 = allData[allData.EpochDate.apply(lambda x: (x >= epoch_start) & (x < epoch_end) )]

        correl = pd.DataFrame(dict(
            Metric=target_list
        ))
        stage_list = ['allData']
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

                sig = determine_signficance(p, target_list)

                exec(f"{stage}_SR.append(r)")
                exec(f"{stage}_PVALUE.append(p)")
                exec(f"{stage}_isSig.append(sig)")

        for stage in stage_list:

            exec(f"correl['{stage}_SR'] = {stage}_SR")
            exec(f"correl['{stage}_isSig'] = {stage}_isSig")
            exec(f"correl['{stage}_PVALUE'] = {stage}_PVALUE")

            correl[f'{stage}_SR'] = correl[f'{stage}_SR'].apply(
                lambda x: round_value(x))
            correl[f'{stage}_PVALUE'] = correl[f'{stage}_PVALUE'].apply(
                lambda x: round_value(x))

            exec(
                f"correl['{stage}_SR'] = correl['{stage}_SR'].astype(str) + correl['{stage}_isSig']")

            exec(f"del correl['{stage}_isSig']")

        print("correlation \n ")
        print(correl)

        return(correl)

    # for shift in [0,-1,-2]:

    correlations(
        term='no_submissions',
        target_list=target_list,
        combData=combData,
        shift=0).to_csv("saving_test.csv", index=False)


# get_reddit_crypto_corre(1634403579, 1644757979, 'ETHUSDT', 'Crypto_General')
