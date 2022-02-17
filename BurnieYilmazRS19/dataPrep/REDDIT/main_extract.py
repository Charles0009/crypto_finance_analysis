from dataExtracting1 import data_extracting
from textProcessing2 import textprocess
from dailyWordFreq3 import dailywordfreq

import datetime


start = 1601251200
end =   1620495694
subreddit= 'Bitcoin'

start_in_date = datetime.datetime.fromtimestamp(start)
end_in_date = datetime.datetime.fromtimestamp(end)
print(start_in_date)
print(end_in_date)


start_in_date = str(start_in_date)
end_in_date = str(end_in_date)
start_in_date = start_in_date[:10]
end_in_date = end_in_date[:10]

name_for_file = subreddit+"_"+start_in_date+"_"+end_in_date
name_for_file_extracting = '/mnt/c/Users/charl/Desktop/finance_perso/BurnieYilmazRS19/dataPrep/REDDIT/data/extracting/'+name_for_file+'.pkl'
name_for_saving_processed = '/mnt/c/Users/charl/Desktop/finance_perso/BurnieYilmazRS19/dataPrep/REDDIT/data/processing/tokenFreq/'+name_for_file+'.pkl'



data_extracting( start=start, 
                 end=end ,
                 subreddit=subreddit,
                 name_for_file_extracting = name_for_file_extracting )

textprocess(name_for_file_extracting)
dailywordfreq( start=start, 
                end=end, 
                name_for_saving_processed = name_for_saving_processed   )
