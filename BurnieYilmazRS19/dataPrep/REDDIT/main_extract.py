from dataExtracting1 import data_extracting
from textProcessing2 import textprocess
from dailyWordFreq3 import dailywordfreq
import os

import datetime


start = 1634251200
end =   1644830527
subreddit= 'CryptoMarkets'

start_in_date = datetime.datetime.fromtimestamp(start)
end_in_date = datetime.datetime.fromtimestamp(end)
print(start_in_date)
print(end_in_date)


start_in_date = str(start_in_date)
end_in_date = str(end_in_date)
start_in_date = start_in_date[:10]
end_in_date = end_in_date[:10]

current_directory = str(os.getcwd())

name_for_file = subreddit+"_"+start_in_date+"_"+end_in_date
name_for_file_extracting = current_directory+'/BurnieYilmazRS19/dataPrep/REDDIT/data/extracting/'+name_for_file+'.pkl'

print(name_for_file_extracting)

name_for_saving_processed = current_directory+'/BurnieYilmazRS19/dataPrep/REDDIT/data/processing/tokenFreq/'+name_for_file+'.pkl'


#call to the api for extraction
print("data extracting")
data_extracting( start=start, 
                 end=end ,
                 subreddit=subreddit,
                 name_for_file_extracting = name_for_file_extracting )
#call to the api for extraction
print("text processing")
textprocess(name_for_file_extracting)
print("daily word frequency")
dailywordfreq( start=start, 
                end=end, 
                name_for_saving_processed = name_for_saving_processed   )

print(name_for_saving_processed)
