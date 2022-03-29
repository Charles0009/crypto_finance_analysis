import os
import sys

working_dir = str(os.getcwd())

# Insert the path of modules folder 
sys.path.insert(0, working_dir+'/BurnieYilmazRS19/dataPrep/REDDIT/' )

from  dataExtracting1 import data_extracting
from textProcessing2 import textprocess
from  dailyWordFreq3 import dailywordfreq




import datetime


# start = 1634251200
# end =   1644830527
# subreddit= 'CryptoMarkets'


def extract_full_reddit_token_frequency(start_epoch, end_epoch, subreddit):
   
    start_in_date = datetime.datetime.fromtimestamp(start_epoch)
    end_in_date = datetime.datetime.fromtimestamp(end_epoch)
    print(" start date : " + str(start_in_date))
    print(" start date : " + str(end_in_date))


    start_in_date = str(start_in_date)
    end_in_date = str(end_in_date)
    start_in_date = start_in_date[:10]
    end_in_date = end_in_date[:10]

    current_directory = str(os.getcwd())

    name_for_file = subreddit+"_"+start_in_date+"_"+end_in_date
    name_for_file_extracting = current_directory+'/BurnieYilmazRS19/dataPrep/REDDIT/data/extracting/'+name_for_file+'.pkl'

    print("name for file extracting : " + name_for_file_extracting)

    name_for_saving_processed = current_directory+'/BurnieYilmazRS19/dataPrep/REDDIT/data/processing/tokenFreq/'+name_for_file+'.pkl'

    print("name for file processing : " + name_for_saving_processed)

    #call to the api for extraction
    print("data extracting")
    data_extracting( start=start_epoch, 
                    end=end_epoch ,
                    subreddit=subreddit,
                    name_for_file_extracting = name_for_file_extracting )
    #call to the api for extraction
    print("text processing")
    textprocess(name_for_file_extracting)
    print("daily word frequency")
    dailywordfreq( start=start_epoch, 
                    end=end_epoch, 
                    name_for_saving_processed = name_for_saving_processed   )

    print("name for save file : " + name_for_saving_processed)

    return(name_for_saving_processed)