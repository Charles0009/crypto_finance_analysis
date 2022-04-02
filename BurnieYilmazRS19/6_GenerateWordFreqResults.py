# ----------------------------------------------------------------------------------
# # Word Frequency Results CSV Creation
# ----------------------------------------------------------------------------------

import pandas as pd
import numpy as np
import time
import matplotlib.pyplot as plt
import multiprocessing
import sys
import os
import time
from calendar import timegm

working_dir = str(os.getcwd())

# Insert the path of modules folder 
sys.path.insert(0, working_dir+'/BurnieYilmazRS19/dataPrep/REDDIT/' )
sys.path.insert(0, working_dir+'/finance_calc/' )



from scipy.stats import mannwhitneyu 
from main_extract import extract_full_reddit_token_frequency
from find_periods import cut_period_into_trends




print("Load Data")


def get_word_freq_results_csv(pair, start_date, end_date, subreddit):


    if type(start_date) == int:
        start_text = pd.to_datetime(start_date, unit='s')
        start_text = start_text.strftime("%d %b %Y") 
        end_text = pd.to_datetime(end_date, unit='s')
        end_text = end_text.strftime("%d %b %Y") 

    else:
        print('did nothing to transform dates')

    filepath = extract_full_reddit_token_frequency(
            start_date, end_date, subreddit)
    wordFreqData = pd.read_pickle(filepath)
    # name_for_saving_processed = working_dir+'/BurnieYilmazRS19/dataPrep/REDDIT/data/processing/tokenFreq/'+name_for_file+'.pkl'
    # wordFreqData = pd.read_pickle(working_dir + '/BurnieYilmazRS19/dataPrep/REDDIT/data/processing/tokenFreq/Crypto_General_2021-10-16_2022-02-13.pkl')

    print("Splitting Data and Descriptive Statistics")

######################################################################################################################################################################################################################

    sub_count = dict()

    sub_count['ALL'] = sum(wordFreqData['no_submissions'])

    #From inclusive to before
    # divide into periods of growth and recession 

    liste_periods = cut_period_into_trends(pair, start_text, end_text, 0)

    # liste_periods = cut_period_into_trends("BTCUSDT", "2021-10-16", "2022-02-13", 0)
    o =0
    liste_length =[]
    liste_of_subs = []
    liste_length.append(len(wordFreqData))

    while o < (len(liste_periods) - 1):
        dataframe_sub = wordFreqData[wordFreqData.day_time_stamp.apply(lambda x: (x >= (liste_periods[o][2]+7200) ) & (x < (liste_periods[o+1][2]+7200) ) )]

        if liste_periods[o][3] == 'resistance':
            name_for_section = 'down'
        elif liste_periods[o][3] == 'support':
            name_for_section = 'up'

        start_time_text = pd.to_datetime((liste_periods[o][2]+7200), unit='s')
        start_time_text = start_time_text.strftime("%d_%b_%Y")
        end_time_text = pd.to_datetime((liste_periods[o+1][2]+7200), unit='s')
        end_time_text = end_time_text.strftime("%d_%b_%Y") 
        name_for_section = name_for_section + '_' +start_time_text+'_' + end_time_text

        liste_of_subs.append(dataframe_sub)

        liste_length.append(len(dataframe_sub))

        sub_count[name_for_section] = sum(dataframe_sub['no_submissions'])

        o+=1

## find an algorithm to analyse/find periods of growth and decrease in price 


    descData = pd.DataFrame(dict(
        dates = list(sub_count.keys()),
        no_submissions = list(sub_count.values()),
        no_days = liste_length
    ))


    descData['subPerDay'] = descData['no_submissions']/descData['no_days']

    name_for_saving_first_file = 'descriptive_stats' + pair + subreddit + start_text + end_text

    descData.to_csv(working_dir + '/BurnieYilmazRS19/resultsData/' + name_for_saving_first_file+'.csv')

    del descData

    #############################################################################################################################################################

    print("Frequency Data")

    names = wordFreqData.columns.values.tolist()

    names.remove('day_time_stamp')
    names.remove('no_submissions')

    print("NO TOKENS:", len(names))

    #Remove tokens in <= 100 submissions:

    subsetnames = list(filter(lambda x: (sum(wordFreqData[x]) > 100), names))

    print("NO TOKENS AFTER FILTERING:", len(subsetnames))

    print(subsetnames)

    print("TOTALS DATA")

    total_data = pd.DataFrame()

    for i, name in enumerate(subsetnames):
        total_data.at[i, 'token']  = name
        total_data.at[i, 'tot_all'] = sum(wordFreqData[name])/sum(wordFreqData['no_submissions']) * 100
        p = 0
        while p < (len(liste_of_subs) - 1):
            name_for_section = 'tot_p'+str(p)
            total_data.at[i, name_for_section] = sum(liste_of_subs[p][name])/sum(liste_of_subs[p]['no_submissions']) * 100
            p+=1

        print((i+1)/len(subsetnames), '...........................', end='\r')

    # total_data.to_csv('/mnt/c/Users/charl/Desktop/finance_perso/BurnieYilmazRS19/resultsData/percent_totals_long_terms_Bitcoin.csv')

    name_for_saving_second_file = 'percent_totals' + pair + subreddit + start_text + end_text

    total_data.to_csv(working_dir + '/BurnieYilmazRS19/resultsData/' + name_for_saving_second_file+'.csv')



################################################################################################################################################################################################

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

    # WC_data = pd.DataFrame()

    # for i, name in enumerate(subsetnames):
    #     WC_data.at[i, 'token']  = name

    #     l = 0
    #     while l < (len(liste_of_subs) - 1):

    #         WC_data.at[i, 'change_p1_p2'] = per_change(index=i, col1='tot_p1', col2='tot_p2')
    #         WC_data.at[i, 'wc_p1_p2'] = pValueGen(p1,p2,name,alternative_th='two-sided')

    #         l += 1




    #     try:
    #         WC_data.at[i, 'change_p1_p2'] = per_change(index=i, col1='tot_p1', col2='tot_p2')
    #         WC_data.at[i, 'wc_p1_p2'] = pValueGen(p1,p2,name,alternative_th='two-sided')
            
    #         WC_data.at[i, 'change_p2_p3'] = per_change(index=i, col1='tot_p2', col2='tot_p3')
    #         WC_data.at[i, 'wc_p2_p3'] = pValueGen(p2,p3,name,alternative_th='two-sided')

    #         WC_data.at[i, 'change_p3_p4'] = per_change(index=i, col1='tot_p3', col2='tot_p4')
    #         WC_data.at[i, 'wc_p3_p4'] = pValueGen(p3,p4,name,alternative_th='two-sided')

    #         WC_data.at[i, 'change_p4_p5'] = per_change(index=i, col1='tot_p4', col2='tot_p5')
    #         WC_data.at[i, 'wc_p4_p5'] = pValueGen(p4,p5,name,alternative_th='two-sided')

    #         WC_data.at[i, 'change_p5_p6'] = per_change(index=i, col1='tot_p5', col2='tot_p6')
    #         WC_data.at[i, 'wc_p5_p6'] = pValueGen(p5,p6,name,alternative_th='two-sided')

    #         WC_data.at[i, 'change_p6_p7'] = per_change(index=i, col1='tot_p6', col2='tot_p7')
    #         WC_data.at[i, 'wc_p6_p7'] = pValueGen(p6,p7,name,alternative_th='two-sided')

    #         WC_data.at[i, 'change_p7_p8'] = per_change(index=i, col1='tot_p7', col2='tot_p8')
    #         WC_data.at[i, 'wc_p7_p8'] = pValueGen(p7,p8,name,alternative_th='two-sided')

    #         WC_data.at[i, 'change_p8_p9'] = per_change(index=i, col1='tot_p8', col2='tot_p9')
    #         WC_data.at[i, 'wc_p8_p9'] = pValueGen(p8,p9,name,alternative_th='two-sided')

    #         WC_data.at[i, 'change_p9_p10'] = per_change(index=i, col1='tot_p9', col2='tot_p10')
    #         WC_data.at[i, 'wc_p9_p10'] = pValueGen(p9,p10,name,alternative_th='two-sided')

    #         WC_data.at[i, 'change_p10_p11'] = per_change(index=i, col1='tot_p10', col2='tot_p11')
    #         WC_data.at[i, 'wc_p10_p11'] = pValueGen(p10,p11,name,alternative_th='two-sided')

    #     except:
    #         print("")

    #     print((i+1)/len(subsetnames), '...........................', end='\r')


    # WC_data.to_csv('/mnt/c/Users/charl/Desktop/finance_perso/BurnieYilmazRS19/resultsData/wilcoxon_rank_long_terms_Bitcoin.csv')
    
    # name_for_saving_third_file = 'wilcoxon_rank' + pair + subreddit + start_text + end_text

    # total_data.to_csv(working_dir + '/BurnieYilmazRS19/resultsData/' + name_for_saving_third_file+'.csv')





get_word_freq_results_csv('ETHUSDT', 1634256000, 1640995200, 'CryptoCurrencies')