import os 
import sys
from datetime import datetime

working_dir = str(os.getcwd())
print(working_dir)
# Insert the path of modules folder
working_dir = str(os.getcwd())
print(working_dir)
# Insert the path of modules folder

try : 

    sys.path.insert(0, working_dir+'/BurnieYilmazRS19/' )
    sys.path.insert(0, working_dir+'/BurnieYilmazRS19/dataPrep/VADER/' )
    
    from GenerateWordFreqResults import get_word_freq_results_csv
    from VADER import plot_vader_values
    from VADER import get_list_of_words_of_interest
    from VADER_terms import get_vader_terms_csv

except ModuleNotFoundError :
    try:
        sys.path.insert(0, working_dir+'/crypto_finance_anlysis/BurnieYilmazRS19/' )
        sys.path.insert(0, working_dir+'/crypto_finance_anlysis/BurnieYilmazRS19/dataPrep/VADER/' )

        from GenerateWordFreqResults import get_word_freq_results_csv
        from VADER import plot_vader_values
        from VADER import get_list_of_words_of_interest
        from VADER_terms import get_vader_terms_csv
        
    except ModuleNotFoundError :
        sys.path.insert(0, working_dir+'/' )

        from GenerateWordFreqResults import get_word_freq_results_csv
        from VADER import plot_vader_values
        sys.path.insert(0, working_dir+'/dataPrep/VADER/' )
        from VADER import get_list_of_words_of_interest
        from VADER_terms import get_vader_terms_csv



crypto_couple = 'BTCUSDT'
start_date_epoch =  1648771200
end_date_epoch = 1659312000
subreddit_name = 'CryptoCurrencies'
time_interval= '3days'

# path_to_pkl_data= working_dir+'/dataPrep/REDDIT/data/extracting/CryptoCurrencies_2022-04-17_2022-06-17.pkl'
path_to_pkl_data= working_dir+'/dataPrep/REDDIT/data/extracting/CryptoCurrencies_2021-02-01_2022-02-01.pkl'


# path_to_pkl_data1= working_dir+'/dataPrep/REDDIT/data/processing/tokenFreq/CryptoCurrencies_2022-04-17_2022-06-17.pkl'
path_to_pkl_data1= working_dir+'/dataPrep/REDDIT/data/processing/tokenFreq/CryptoCurrencies_2021-02-01_2022-02-01.pkl'

print(working_dir)
# start_date_epoch = 1650204350
# end_date_epoch = 1655474750
start_date_epoch = 1612197402
end_date_epoch = 1643733402
# path_to_pkl_data= filepath

interval_in_seconds = 86400

start_date = start_date_epoch
end_date = end_date_epoch
liste_timing_infos = list(range(start_date, end_date, interval_in_seconds))

liste_of_words = get_list_of_words_of_interest(path_to_pkl_data1, threshold_num_submissions = 500)
print(liste_of_words)
file_path_csv_vader = get_vader_terms_csv(path_to_pkl_data, liste_of_words, liste_timing_infos, crypto_couple, subreddit_name, start_date_epoch, end_date_epoch)
# file_path_csv_vader = working_dir+'/dataPrep/VADER/vader_BNBUSDT_CryptoCurrencies_1650204350_1655474750.csv'
# liste_of_words = ["tax", "ban", "bitcoin"]
df = plot_vader_values(file_path_csv_vader, liste_of_words,crypto_couple, subreddit_name, start_date_epoch, end_date_epoch,path_to_pkl_data1, plot_or_not = False, study_window = 6)

