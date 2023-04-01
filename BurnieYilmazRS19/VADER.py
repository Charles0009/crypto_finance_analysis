# ----------------------------------------------------------------------------------
# # Presents VADER sentiment results
# ----------------------------------------------------------------------------------

import pandas as pd 
import matplotlib.pyplot as plt
from matplotlib.dates import AutoDateFormatter, AutoDateLocator, date2num
import time
import matplotlib.dates as mdate
import os 
import sys
import time
from pathlib import Path
import argparse
from collections import defaultdict
import warnings


warnings.simplefilter(action='ignore', category=pd.errors.PerformanceWarning)


print("TERMS-RESTRICTED SUBMISSIONS")


working_dir = str(os.getcwd())

def get_list_of_words_of_interest(path_to_pkl_data,threshold_num_submissions):
    
    wordFreq = pd.read_pickle(path_to_pkl_data)
    i = 0
    dic_of_mentionned_words = {}

    for col in wordFreq.columns:
        if col == "day_time_stamp":
            continue
        if col == "no_submissions":
            continue
        if wordFreq[col].sum()>threshold_num_submissions:
            i+=1
            dic_of_mentionned_words[col] = wordFreq[col].sum()


    print('len list of relevant numerically terms : ', i)
    # print(wordFreq.head())

    dic_of_mentionned_words_sorted = sorted(dic_of_mentionned_words.items(), key=lambda x:x[1], reverse=True)
    # print(dic_of_mentionned_words_sorted)

    liste_of_mentionned_words = [i[0] for i in dic_of_mentionned_words_sorted if i[0].isdigit()==False]


    return liste_of_mentionned_words



def plot_vader_values(file_path, liste_of_words,crypto_couple, subreddit_name, start_date_epoch, end_date_epoch, path_to_pkl_data, plot_or_not, study_window): 

    VADERterms = pd.read_csv(file_path)
    wordFreq = pd.read_pickle(path_to_pkl_data)
    working_dir = str(os.getcwd())
    
    # print(wordFreq.head())
    # print("working_dir : ", working_dir)

    # Insert the path of modules folder 
    try :
            sys.path.insert(0, working_dir+'/apis/' )
            sys.path.insert(0, working_dir+'/BurnieYilmazRS19/' )
            from  get_data_api_b import get_pd_daily_histo_between_dates
            from termTracker import TrendDrawer
    except ModuleNotFoundError :
            try: 
                    sys.path.insert(0, working_dir+'/crypto_finance_anlysis/apis/' )
                    sys.path.insert(0, working_dir+'/crypto_finance_anlysis/BurnieYilmazRS19/' )
                    from  get_data_api_b import get_pd_daily_histo_between_dates
                    from termTracker import TrendDrawer
            except ModuleNotFoundError :
                    path_for_finance_calc = Path(working_dir).parent
                    sys.path.insert(0, str(path_for_finance_calc)+'/apis/' )
                    sys.path.insert(0, working_dir+'/BurnieYilmazRS19/' )
                    from  get_data_api_b import get_pd_daily_histo_between_dates
                    from termTracker import TrendDrawer
                    

    df_price_couple = get_pd_daily_histo_between_dates(crypto_couple, start_date_epoch, end_date_epoch)
    print("crypto_couple : ", crypto_couple)
    df_price_couple = df_price_couple.rename(columns={"epoch_time": "EpochDate"})

    def get_begining_of_num(x): 
        str2 = str(x)[0:5]
        return str2

    df_price_couple['abbreviated_epoch'] = df_price_couple['EpochDate'].apply(lambda x: get_begining_of_num(x))
    VADERterms['abbreviated_epoch'] = VADERterms['EpochDate'].apply(lambda x: get_begining_of_num(x))


    VADERterms = pd.merge(VADERterms,df_price_couple[['abbreviated_epoch','mean_daily_price']],on='abbreviated_epoch', how='left')


    # print(wordFreq.head())
    wordFreq = wordFreq.rename(columns={"day_time_stamp": "EpochDate"})
    # print("wordFreq", wordFreq.head())
    for word in liste_of_words:
        VADERterms = pd.merge(VADERterms,wordFreq[['EpochDate',word]],on='EpochDate', how='left')
        



    del VADERterms['Unnamed: 0']

    # print("ALL NEG / NEG + POS")
    VADERterms['date'] = mdate.epoch2num(VADERterms['EpochDate'])

    for word in liste_of_words:
        VADERterms[f'{word}_ALLNEG'] = (VADERterms[f'{word}_NEG']).rolling(study_window).sum()
        VADERterms[f'{word}_ALLPOS'] = (VADERterms[f'{word}_POS']).rolling(study_window).sum()
        VADERterms[f'{word}_ALLNEU'] = (VADERterms[f'{word}_NEU']).rolling(study_window).sum()
        VADERterms[f'{word}_NEG_RATIO'] =  VADERterms[f'{word}_ALLNEG'] / (VADERterms[f'{word}_ALLPOS'] + VADERterms[f'{word}_ALLNEG']+ VADERterms[f'{word}_ALLNEU'])
        VADERterms[f'{word}_POS_RATIO'] =  VADERterms[f'{word}_ALLPOS'] / (VADERterms[f'{word}_ALLPOS'] + VADERterms[f'{word}_ALLNEG'] + VADERterms[f'{word}_ALLNEU'])


    def columns_ordering(df):
        cols = df.columns.tolist()
        cols = sorted(cols)
        df = df[cols]
        return df
    
    
    
    VADERterms = columns_ordering(VADERterms)
    
    
    VADERterms = VADERterms.drop('abbreviated_epoch', axis=1)
    VADERterms = VADERterms.drop('date', axis=1)

    first_column = VADERterms.pop('no_submissions')
    VADERterms.insert(0, 'no_submissions', first_column)

    first_column = VADERterms.pop('mean_daily_price')
    VADERterms.insert(0, 'mean_daily_price', first_column)

    first_column = VADERterms.pop('EpochDate')
    VADERterms.insert(0, 'EpochDate', first_column)
    
    VADERterms = VADERterms.convert_dtypes()

    if plot_or_not == True:
        str_path_for_jpeg_save_file = crypto_couple+"_"+ subreddit_name+"_" +str(start_date_epoch)+"_"+ str(end_date_epoch) + ".jpeg"
        for word in liste_of_words:
            

            grid = plt.GridSpec(2, 1, hspace=0.2, wspace=0.2)
            fig = plt.figure(figsize=(12, 7))


            ax1 = fig.add_subplot(grid[0])
            l1, = ax1.plot(VADERterms['date'], VADERterms[f'{word}_NEG_RATIO']*100,linestyle = '-', marker = "", color='red',label='negative') #Your Price field
            l3, = ax1.plot(VADERterms['date'], VADERterms[f'{word}_POS_RATIO']*100,linestyle = '-', marker = "", color='green',label='positive') #Your Price field

            ax1.set_ylabel('percentage')
            ax2 = ax1.twinx() ##Using twinx to make ax2 as secondary axis for ax1
            l2, = ax2.plot(VADERterms['date'], VADERterms['mean_daily_price'], linestyle = '--',marker = "", color='k') 
            ax2.set_ylabel('price')

            fig.legend([l3, l1, l2], [ "positve", "negative", "price"])

            ax1.xaxis.set_ticks([])
            ax2.xaxis.set_ticks([])
            ax1.set_title(word + " sentiment and " + crypto_couple +" price")
            


            ax3= fig.add_subplot(grid[1, 0], sharex=ax1)
            ax3.bar(VADERterms['date'],VADERterms[word] , color='gray')
            xtick_locator = AutoDateLocator()
            xtick_formatter = AutoDateFormatter(xtick_locator)

            ax3.xaxis.set_major_locator(xtick_locator)
            ax3.xaxis.set_major_formatter(xtick_formatter)
            ax3.set_title("# of submissions", y=-0.01)
            ax3.invert_yaxis()
            ax3.tick_params(labelrotation=45)

            
            plt.tight_layout()

            try: 
                name_1 = f'/BurnieYilmazRS19/visuals/VADER/{word}_test_VADER_'
                name_for_saving = working_dir+ name_1  + str_path_for_jpeg_save_file
                # print('name saving jpeg files ' + name_for_saving)
                plt.savefig(name_for_saving)
            except FileNotFoundError: 
                name_1 = f'/visuals/VADER/{word}_test_VADER_'
                name_for_saving = working_dir+ name_1  + str_path_for_jpeg_save_file
                # print('name saving jpeg files ' + name_for_saving)
                plt.savefig(name_for_saving)
            # plt.savefig(f'../BurnieYilmazRS19/visuals/VADER/{word}_test_VADER.jpeg')
            plt.close()

            
    return VADERterms

# liste_of_words = ["bitcoin", "tax", "ban", "DMS"]
# liste_of_words = ['crypto', 'dollar_marker_symbol', 'bitcoin', 'cryptocurr', 'new', 'market', 'token', 'terra', 'luna', 'invest', 'get', 'go', 'nft', 'use', 'make', 'project', 'trade', 'coin', 'launch', 'blockchain', 'exchang', 'say', 'ethereum', 'wallet', 'earn', 'price', 'know', 'like', 'buy', 'mine', 'one', 'time']
# file_path = working_dir+'/BurnieYilmazRS19/dataPrep/VADER/vader_BNBUSDT_CryptoCurrencies_1650204350_1655474750.csv'
# crypto_couple = 'BNBUSDT'
# start_date_epoch =  1650204350
# end_date_epoch = 1655474750
# subreddit_name = 'CryptoCurrencies'
# path_to_pkl_data = working_dir+'/BurnieYilmazRS19/dataPrep/REDDIT/data/processing/tokenFreq/CryptoCurrencies_2022-04-17_2022-06-17.pkl'

# # liste = get_list_of_words_of_interest(path_to_pkl_data, threshold_num_submissions = 50)
# # print(liste)

# df = plot_vader_values(file_path, liste_of_words,crypto_couple, subreddit_name, start_date_epoch, end_date_epoch, path_to_pkl_data, False)

# print(df.head(5


