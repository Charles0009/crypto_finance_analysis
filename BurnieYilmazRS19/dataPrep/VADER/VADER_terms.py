import pandas as pd
from datetime import datetime
from concurrent.futures import ProcessPoolExecutor
from multiprocessing import freeze_support
from functools import partial

from helper.helper import helper

import sys
import os



working_dir = str(os.getcwd())

# Insert the path of modules folder

try : 

    sys.path.append(working_dir+'/BurnieYilmazRS19/dataPrep/REDDIT/')

    from text.processing import SentenceProcessor
    from text.dataHandling import DataHandling



except ModuleNotFoundError :
    try:
        sys.path.insert(0, working_dir+'/crypto_finance_anlysis/BurnieYilmazRS19/dataPrep/REDDIT/' )

        from text.processing import SentenceProcessor
        from text.dataHandling import DataHandling
    except ModuleNotFoundError :
        sys.path.insert(0, working_dir+'/dataPrep/REDDIT/' )
        from text.processing import SentenceProcessor
        from text.dataHandling import DataHandling





from nltk.sentiment.vader import SentimentIntensityAnalyzer as SIA


def termProcessor(term=False,data=None): 
    # print("*************************************")
    # print("term : ", term)
    # print("data : ", data)
    # print("*************************************")

    return(
        data.text.apply(lambda x: x.lower())
            .apply(SentenceProcessor.removelongText)
            .apply(SentenceProcessor.removeURL)
            .apply(SentenceProcessor.removeHTMLCharacterEntities)
            .apply(SentenceProcessor.removeLineJump)
            .apply(SentenceProcessor.removeRemovedDeleted)
            .apply(SentenceProcessor.standardiseTransactions)
            .apply(lambda x: helper.categoriser(submission_text=x, filterer=helper.submission_filterer, processor=helper.sentimentProcessor, term=term))
    )


def get_vader_terms_csv(path_to_pkl_data, liste_of_words, liste_timing_infos,  crypto_couple, subreddit_name, start_date_epoch, end_date_epoch):
    freeze_support()
    

    print("Submissions data loaded - ", datetime.now())
    dataObj = DataHandling(data_frame = pd.read_pickle(path_to_pkl_data))
    dataObj.removeExcludedRows()
    dataObj.splitData(step=10000)

    for word in liste_of_words:
        
        termProcessor2 = partial(termProcessor, word)  
        # print("Begin data processing - ", datetime.now())
        with ProcessPoolExecutor() as executor:
            textList = executor.map(termProcessor2, dataObj.getDataList(), chunksize = 3)
        # print("Begin data storing - ", datetime.now())        
        for i, text in enumerate(textList):
            dataObj.getDataList()[i][f'{word}_VADER'] = text
            
        del textList

    dataObj.aggData()
    data = dataObj.selectFirstFrame()
    del dataObj

    print("REMOVE SUBMISSIONS BLANK AFTER PROCESSING")
    data = data[data.text.apply(lambda x: x != [])]

    sentimentData = pd.DataFrame()

    EpochDate_list = []
    no_submissions_list = []

    for word in liste_of_words:
        exec(f"{word}_NEG_list = []")
        exec(f"{word}_NEU_list = []")
        exec(f"{word}_POS_list = []")

    
    print("Counting labels for each term")       


    labelCounter2 = partial(helper.labelCounterTerms, [data, liste_of_words])
    
    # args = ((liste_timing_infos, liste_of_words) for liste_of_words in c)

    with ProcessPoolExecutor() as executor:
        sentiments = executor.map(labelCounter2, liste_timing_infos, chunksize = 10)

    # print("sentiments : ", sentiments)
    for i in sentiments:
        EpochDate_list.append(i['EpochDate'])
        no_submissions_list.append(i['no_submissions'])
        for word in liste_of_words:
            exec(f"{word}_NEG_list.append(i['{word}_NEG'])")
            exec(f"{word}_NEU_list.append(i['{word}_NEU'])")
            exec(f"{word}_POS_list.append(i['{word}_POS'])")
        
    sentimentData['EpochDate'] = EpochDate_list
    sentimentData['no_submissions'] = no_submissions_list

    for word in liste_of_words:          
        exec(f"sentimentData['{word}_NEG'] = {word}_NEG_list")
        exec(f"sentimentData['{word}_NEU'] = {word}_NEU_list")
        exec(f"sentimentData['{word}_POS'] = {word}_POS_list")
    
    try: 
        str_path_for_csv_save_file = working_dir+'/BurnieYilmazRS19/dataPrep/VADER/'+ "vader_"+ crypto_couple+"_"+ subreddit_name+"_" +str(start_date_epoch)+"_"+ str(end_date_epoch) + '.csv'
        sentimentData.to_csv(str_path_for_csv_save_file)
    except OSError :
        str_path_for_csv_save_file = working_dir+'/dataPrep/VADER/'+ "vader_"+ crypto_couple+"_"+ subreddit_name+"_" +str(start_date_epoch)+"_"+ str(end_date_epoch) + '.csv'
        sentimentData.to_csv(str_path_for_csv_save_file)
    

    print('path for saving vader file :' + str_path_for_csv_save_file)

    return str_path_for_csv_save_file



# path_to_pkl_data= working_dir+'/BurnieYilmazRS19/dataPrep/REDDIT/data/extracting/CryptoCurrencies_2022-04-17_2022-06-17.pkl'
# liste_of_words = ['crypto', 'dollar_marker_symbol', 'bitcoin', 'cryptocurr', 'new', 'market', 'token', 'terra', 'luna', 'invest', 'get', 'go', 'nft', 'use', 'make', 'project', 'trade', 'coin', 'launch', 'blockchain', 'exchang', 'say', 'ethereum', 'wallet', 'earn', 'price', 'know', 'like', 'buy', 'mine', 'one', 'time']
# crypto_couple = 'BNBUSDT'
# start_date_epoch =  1650204350
# end_date_epoch = 1655474750
# subreddit_name = 'CryptoCurrencies'
# start_date = start_date_epoch
# end_date = end_date_epoch
# interval_in_seconds = 86400

# liste_timing_infos = list(range(start_date, end_date, interval_in_seconds))


# get_vader_terms_csv(path_to_pkl_data, liste_of_words, liste_timing_infos, crypto_couple, subreddit_name, start_date_epoch, end_date_epoch)