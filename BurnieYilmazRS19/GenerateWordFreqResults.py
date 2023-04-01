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
from scipy.stats import mannwhitneyu 
from pathlib import Path


print("Load Data")


def get_word_freq_results_csv(pair, start_date, end_date, subreddit, precision_periods):

    working_dir = str(os.getcwd())
    print("working_dir /////////////////////" + working_dir)

    # Insert the path of modules folder

    try : 

        sys.path.insert(0, working_dir+'/BurnieYilmazRS19/dataPrep/REDDIT/' )
        sys.path.insert(0, working_dir+'/finance_calc/' )
        from main_extract import extract_full_reddit_token_frequency
        from find_periods import cut_period_into_trends

    except ModuleNotFoundError :
        try:
            sys.path.insert(0, working_dir+'/crypto_finance_anlysis/BurnieYilmazRS19/dataPrep/REDDIT/' )
            sys.path.insert(0, working_dir+'/crypto_finance_anlysis/finance_calc/' )
            from main_extract import extract_full_reddit_token_frequency
            from find_periods import cut_period_into_trends
        except ModuleNotFoundError :
            sys.path.insert(0, working_dir+'/dataPrep/REDDIT/' )
            path_for_finance_calc = Path(working_dir).parent
            sys.path.insert(0, str(path_for_finance_calc)+'/finance_calc/' )

            from main_extract import extract_full_reddit_token_frequency
            from find_periods import cut_period_into_trends



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
    # wordFreqData = pd.read_pickle(working_dir + '/BurnieYilmazRS19/dataPrep/REDDIT/data/processing/tokenFreq/CryptoCurrencies_2021-02-01_2022-02-01.pkl')

    print("Splitting Data and Descriptive Statistics")

######################################################################################################################################################################################################################

    sub_count = dict()

    sub_count['ALL'] = sum(wordFreqData['no_submissions'])

    #From inclusive to before
    # divide into periods of growth and recession 

    liste_periods = cut_period_into_trends(pair, start_text, end_text, 0, precision_periods)

    #liste_periods = cut_period_into_trends("BTCUSDT", "2021-10-16", "2022-02-13", 0, '3days')

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
    try : 
        descData.to_csv(working_dir + '/BurnieYilmazRS19/resultsData/' + name_for_saving_first_file+'.csv')
    except :
        descData.to_csv(working_dir + '/crypto_finance_anlysis/BurnieYilmazRS19/resultsData/' + name_for_saving_first_file+'.csv')
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


    print("TOTALS DATA")

    total_data = pd.DataFrame()


    for i, name in enumerate(subsetnames):
        total_data.at[i, 'token']  = name
        total_data.at[i, 'tot_all'] = sum(wordFreqData[name])/sum(wordFreqData['no_submissions']) * 100
        p = 0
        while p < (len(liste_of_subs) - 1):
            name_for_section = 'tot_p'+str(p)
            try: 
                total_data.at[i, name_for_section] = sum(liste_of_subs[p][name])/sum(liste_of_subs[p]['no_submissions']) * 100
            except: 
                print("no subs for the period")
            p+=1

        print((i+1)/len(subsetnames), '...........................', end='\r')

    # total_data.to_csv('/mnt/c/Users/charl/Desktop/finance_perso/BurnieYilmazRS19/resultsData/percent_totals_long_terms_Bitcoin.csv')

    name_for_saving_second_file = 'percent_totals' + pair + subreddit + start_text + end_text
    try :
        total_data.to_csv(working_dir + '/BurnieYilmazRS19/resultsData/' + name_for_saving_second_file+'.csv')
    except :
        total_data.to_csv(working_dir + '/crypto_finance_anlysis/BurnieYilmazRS19/resultsData/' + name_for_saving_second_file+'.csv')



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

    
    WC_data = pd.DataFrame()

    for i, name in enumerate(subsetnames):
        WC_data.at[i, 'token']  = name
        k = 2 
        while k < (total_data.shape[1]-1):
            try:
                name_column1 = 'change_p'+str(k-2) +'_p'+str(k-1)
                name_column2 = 'wc_p'+str(k-2) +'_p'+str(k-1)

                name_investigated_column1 = 'tot_p'+str(k-2)
                name_investigated_column2 = 'tot_p'+str(k-1)
                
                WC_data.at[i, name_column1] = per_change(index=i, col1=name_investigated_column1, col2=name_investigated_column2)
                WC_data.at[i, name_column2] = pValueGen(liste_of_subs[k-2],liste_of_subs[k-1],name,alternative_th='two-sided')
            except:
                print("")

            k+= 1


        print((i+1)/len(subsetnames), '...........................', end='\r')



    # WC_data.to_csv('/mnt/c/Users/charl/Desktop/finance_perso/BurnieYilmazRS19/resultsData/wilcoxon_rank_long_terms_Bitcoin.csv')
    
    name_for_saving_third_file = 'wilcoxon_rank' + pair + subreddit + start_text + end_text
    
    print('NAME FOR SAVING CSV RESULT DATA FILE : ' + working_dir + '/BurnieYilmazRS19/resultsData/' + name_for_saving_third_file+'.csv')

    try : 
        WC_data.to_csv(working_dir + '/BurnieYilmazRS19/resultsData/' + name_for_saving_third_file+'.csv')
    except:
        WC_data.to_csv(working_dir + '/crypto_finance_anlysis/BurnieYilmazRS19/resultsData/' + name_for_saving_third_file+'.csv')

    return filepath




# get_word_freq_results_csv('BTCUSDT', 1648771200, 1659312000, 'CryptoCurrencies', '3days')