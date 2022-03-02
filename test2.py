
import json
import os
import matplotlib.pyplot as plt
from turtle import left
from apis.get_data_api_b import get_list_of_symbols, get_list_of_crypto_names, get_pd_daily_histo_between_dates, change_pair_to_first_crypto_small_cap
from BurnieYilmazRS19.dataPrep.REDDIT.main_extract import extract_full_reddit_token_frequency

import pandas as pd

import datetime


#get token frequency 


start = 1637656969
end =   1640854725
subreddit= 'CryptoCurrency'
#crypto_pair = 'ETHUSDT'





def save_plot_link_relation(start, end, path_to_reddit_file, crypto_pair, path_to_dir_visuals):


    reddit = pd.read_pickle(path_to_reddit_file)

    print(reddit.head())

    df2 = reddit[reddit.columns[reddit.columns.isin( get_list_of_available_cryptos())]]


    df_dates = df2['day_time_stamp']

    name_crypto = change_pair_to_first_crypto_small_cap(crypto_pair, 4)

    # Opening JSON file
    chemin = os.getcwd()
    f = open(chemin+'/crypto_json_names.json')

    # returns JSON object as
    # a dictionary
    data = json.load(f)


    
    try:
        mentions = df2[name_crypto.lower()] + df2[data[name_crypto].lower()]
    except KeyError:
        return ("null")

    df_dates = df_dates.to_frame()
    mentions = mentions.to_frame()

    final_df = df_dates.join(mentions)


    final_df['day_time_stamp'] = pd.to_datetime(final_df['day_time_stamp'], unit='s')
    final_df['day_time_stamp'] = pd.to_datetime(final_df['day_time_stamp']).dt.date
    final_df['day_time_stamp'] = pd.DatetimeIndex(final_df['day_time_stamp']) + pd.DateOffset(1)
    final_df.columns = ['Open_Time', 'nb_mentions']



    start_text = pd.to_datetime(start, unit='s')
    start_text = start_text.strftime("%d %b %Y") 
    end_text = pd.to_datetime(end, unit='s')
    end_text = end_text.strftime("%d %b %Y") 

    try:
        dataframe = get_pd_daily_histo_between_dates(crypto_pair, start_text, end_text)
    except ValueError:
        return('null')
    combined_df = pd.merge(final_df, dataframe, on=['Open_Time'])



    plt.plot(combined_df['Open_Time'], combined_df['Close'], color='blue')
    plt.ylabel('price')
    plt.twinx()
    plt.bar(combined_df['Open_Time'], combined_df['nb_mentions'],color='green')
    plt.ylabel('nb mentions reddit')
    plt.title(crypto_pair)
    #plt.show()

    plt.savefig(path_to_dir_visuals+"/"+crypto_pair+'_'+start_text+'_'+end_text+'.png')

    plt.clf()






def get_list_of_available_cryptos():
    col_list_names_and_symbols = get_list_of_crypto_names()
    col_list_symbol = get_list_of_symbols()
    col_list_symbol = list(map(lambda x: x.lower(), col_list_symbol))
    liste_totale = col_list_names_and_symbols
    liste_totale.append('day_time_stamp')
    liste_totale.append('no_submissions')

    return (liste_totale)


def main():

    liste_of_crypto_to_plot =  get_list_of_available_cryptos()
    liste_of_crypto_to_plot = list(map(lambda x: x.upper(), liste_of_crypto_to_plot))
    new_liste = list()
    for i in range(len(liste_of_crypto_to_plot)):
        if i%2 == 1 :
            element = liste_of_crypto_to_plot[i]
            new_liste.append(element+'USDT')
            
    print(new_liste)


    filepath = extract_full_reddit_token_frequency(start,end, subreddit)


    chemin2 = os.getcwd()
    chemin2= chemin2 + "/export/visuals/"

    # Path
    path = os.path.join(chemin2, subreddit)
    
    print(path)
    os.mkdir(path)


    for name in new_liste:
        print(name)
        save_plot_link_relation(start, end, filepath, name, path)


main()