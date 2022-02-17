# ----------------------------------------------------------------------------------
# # Word Frequency Results CSV Creation
# ----------------------------------------------------------------------------------

import pandas as pd
import numpy as np
import time
import matplotlib.pyplot as plt
import multiprocessing

from scipy.stats import mannwhitneyu 

print("Load Data")

wordFreqData = pd.read_pickle('/mnt/c/Users/charl/Desktop/finance_perso/BurnieYilmazRS19/dataPrep/REDDIT/data/processing/tokenFreq/Bitcoin_2021-05-03_2022-01-03.pkl')

print("Splitting Data and Descriptive Statistics")

sub_count = dict()

sub_count['ALL'] = sum(wordFreqData['no_submissions'])

#From inclusive to before
# divide in 3 to see changes between periods

#GMT: 28 Septembre 2020  -  4 January 2021:
p1 = wordFreqData[wordFreqData.day_time_stamp.apply(lambda x: (x >= 1601251200) & (x < 1609718400) )]

sub_count['28 Septembre 2020  -  4 January 2021'] = sum(p1['no_submissions'])

#GMT:  4 January 2021 -   27 January 2021:
p2 = wordFreqData[wordFreqData.day_time_stamp.apply(lambda x: (x >= 1609718400) & (x < 1611705600) )]

sub_count['4 January 2021 -   27 January 2021'] = sum(p2['no_submissions'])

#GMT: 27 January 2021 - 21 February 2021:
p3 = wordFreqData[wordFreqData.day_time_stamp.apply(lambda x: (x >= 1611705600) & (x < 1613865600) )]

sub_count['27 January 2021 - 21 February 2021'] = sum(p3['no_submissions'])

#GMT: 21 February 2021 - 8 May 2021:
p4 = wordFreqData[wordFreqData.day_time_stamp.apply(lambda x: (x >= 1613865600) & (x < 1620432000) )]

sub_count['21 February 2021 - 8 May 2021'] = sum(p4['no_submissions'])


#GMT: 8 May 2021 - 23 May 2021:
p5 = wordFreqData[wordFreqData.day_time_stamp.apply(lambda x: (x >= 1620432000) & (x < 1621728000) )]

sub_count[' 8 May 2021 - 23 May 2021'] = sum(p5['no_submissions'])


#GMT: 23 May 2021 - 19 July 2021:
p6 = wordFreqData[wordFreqData.day_time_stamp.apply(lambda x: (x >= 1621728000) & (x < 1626652800) )]

sub_count[' 23 May 2021 - 19 July 2021'] = sum(p6['no_submissions'])

#GMT: 19 July 2021 - 13 August 2021:
p7 = wordFreqData[wordFreqData.day_time_stamp.apply(lambda x: (x >= 1626652800) & (x < 1628812800) )]

sub_count['19 July 2021 - 13 August 2021'] = sum(p7['no_submissions'])

#GMT: 13 August 2021 - 28 September 2021:
p8 = wordFreqData[wordFreqData.day_time_stamp.apply(lambda x: (x >= 1628812800) & (x < 1632787200) )]

sub_count['13 August 2021 - 28 September 2021'] = sum(p8['no_submissions'])

#GMT: 28 September 2021 - 20 October 2021:
p9 = wordFreqData[wordFreqData.day_time_stamp.apply(lambda x: (x >= 1632787200) & (x < 1634688000) )]

sub_count['28 September 2021 - 20 October 2021'] = sum(p9['no_submissions'])


#GMT: 20 October 2021 - 25 November 2021:
p10 = wordFreqData[wordFreqData.day_time_stamp.apply(lambda x: (x >= 1634688000) & (x < 1637798400) )]

sub_count['20 October 2021 - 25 November 2021'] = sum(p10['no_submissions'])

#GMT: 25 November 2021 - 2 January 2022:
p11 = wordFreqData[wordFreqData.day_time_stamp.apply(lambda x: (x >= 1637798400) & (x < 1641081600) )]

sub_count['25 November 2021 - 2 January 2022'] = sum(p11['no_submissions'])

""
descData = pd.DataFrame(dict(
    dates = list(sub_count.keys()),
    no_submissions = list(sub_count.values()),
    no_days = [len(wordFreqData), len(p1), len(p2), len(p3), len(p4), len(p5), len(p6), len(p7), len(p8), len(p9), len(p10), len(p11)]
))

descData['subPerDay'] = descData['no_submissions']/descData['no_days']


descData.to_csv('/mnt/c/Users/charl/Desktop/finance_perso/BurnieYilmazRS19/resultsData/descriptiveStats_long_terms_Bitcoin.csv')

del descData

print("Frequency Data")

names = wordFreqData.columns.values.tolist()

names.remove('day_time_stamp')
names.remove('no_submissions')

print("NO TOKENS:", len(names))

#Remove tokens in <= 100 submissions:

subsetnames = list(filter(lambda x: (sum(wordFreqData[x]) > 100), names))

print("NO TOKENS AFTER FILTERING:", len(subsetnames))

print("TOTALS DATA")

total_data = pd.DataFrame()

for i, name in enumerate(subsetnames):
    total_data.at[i, 'token']  = name
    total_data.at[i, 'tot_all'] = sum(wordFreqData[name])/sum(wordFreqData['no_submissions']) * 100
    total_data.at[i, 'tot_p1'] = sum(p1[name])/sum(p1['no_submissions']) * 100
    total_data.at[i, 'tot_p2'] = sum(p2[name])/sum(p2['no_submissions']) * 100
    total_data.at[i, 'tot_p3'] = sum(p3[name])/sum(p3['no_submissions']) * 100
    total_data.at[i, 'tot_p4'] = sum(p4[name])/sum(p4['no_submissions']) * 100
    total_data.at[i, 'tot_p5'] = sum(p5[name])/sum(p5['no_submissions']) * 100
    total_data.at[i, 'tot_p6'] = sum(p6[name])/sum(p6['no_submissions']) * 100
    total_data.at[i, 'tot_p7'] = sum(p7[name])/sum(p7['no_submissions']) * 100
    total_data.at[i, 'tot_p8'] = sum(p8[name])/sum(p8['no_submissions']) * 100
    total_data.at[i, 'tot_p9'] = sum(p9[name])/sum(p9['no_submissions']) * 100
    total_data.at[i, 'tot_p10'] = sum(p10[name])/sum(p10['no_submissions']) * 100
    total_data.at[i, 'tot_p11'] = sum(p11[name])/sum(p11['no_submissions']) * 100

    print((i+1)/len(subsetnames), '...........................', end='\r')

total_data.to_csv('/mnt/c/Users/charl/Desktop/finance_perso/BurnieYilmazRS19/resultsData/percent_totals_long_terms_Bitcoin.csv')

def per_change(index, col1, col2):

        if total_data.at[index, col1] == 0: 
            if total_data.at[index, col2] == 0:
                return(0)
            return(77777777777777777777777777777777777777777777777777777777777777777777777)
        else:
             return(((total_data.at[index, col2] / total_data.at[index, col1]) - 1) * 100)

def pValueGen(data1,data2,word,alternative_th='two-sided'):
        try:
            pValue = mannwhitneyu(data1[word]/data1['no_submissions'], data2[word]/data2['no_submissions'], alternative=alternative_th)[1]
        except ValueError as e:
            print(e)
            pValue = 1 #ensures word not considered in this case as ValueError occurs when word frequencies identical across stages.
        return pValue



print("WILCOXON DATA")

WC_data = pd.DataFrame()

for i, name in enumerate(subsetnames):
    WC_data.at[i, 'token']  = name

    try:
        WC_data.at[i, 'change_p1_p2'] = per_change(index=i, col1='tot_p1', col2='tot_p2')
        WC_data.at[i, 'wc_p1_p2'] = pValueGen(p1,p2,name,alternative_th='two-sided')
        
        WC_data.at[i, 'change_p2_p3'] = per_change(index=i, col1='tot_p2', col2='tot_p3')
        WC_data.at[i, 'wc_p2_p3'] = pValueGen(p2,p3,name,alternative_th='two-sided')

        WC_data.at[i, 'change_p3_p4'] = per_change(index=i, col1='tot_p3', col2='tot_p4')
        WC_data.at[i, 'wc_p3_p4'] = pValueGen(p3,p4,name,alternative_th='two-sided')

        WC_data.at[i, 'change_p4_p5'] = per_change(index=i, col1='tot_p4', col2='tot_p5')
        WC_data.at[i, 'wc_p4_p5'] = pValueGen(p4,p5,name,alternative_th='two-sided')

        WC_data.at[i, 'change_p5_p6'] = per_change(index=i, col1='tot_p5', col2='tot_p6')
        WC_data.at[i, 'wc_p5_p6'] = pValueGen(p5,p6,name,alternative_th='two-sided')

        WC_data.at[i, 'change_p6_p7'] = per_change(index=i, col1='tot_p6', col2='tot_p7')
        WC_data.at[i, 'wc_p6_p7'] = pValueGen(p6,p7,name,alternative_th='two-sided')

        WC_data.at[i, 'change_p7_p8'] = per_change(index=i, col1='tot_p7', col2='tot_p8')
        WC_data.at[i, 'wc_p7_p8'] = pValueGen(p7,p8,name,alternative_th='two-sided')

        WC_data.at[i, 'change_p8_p9'] = per_change(index=i, col1='tot_p8', col2='tot_p9')
        WC_data.at[i, 'wc_p8_p9'] = pValueGen(p8,p9,name,alternative_th='two-sided')

        WC_data.at[i, 'change_p9_p10'] = per_change(index=i, col1='tot_p9', col2='tot_p10')
        WC_data.at[i, 'wc_p9_p10'] = pValueGen(p9,p10,name,alternative_th='two-sided')

        WC_data.at[i, 'change_p10_p11'] = per_change(index=i, col1='tot_p10', col2='tot_p11')
        WC_data.at[i, 'wc_p10_p11'] = pValueGen(p10,p11,name,alternative_th='two-sided')

    except:
        print("")

    print((i+1)/len(subsetnames), '...........................', end='\r')


WC_data.to_csv('/mnt/c/Users/charl/Desktop/finance_perso/BurnieYilmazRS19/resultsData/wilcoxon_rank_long_terms_Bitcoin.csv')




