# ----------------------------------------------------------------------------------
# # Extracting Reddit data from Pushshift API
# ----------------------------------------------------------------------------------

import os
import sys
import pandas as pd
import json
import datetime 


working_dir = str(os.getcwd())

print("working_dir pppp", working_dir)
# Insert the path of modules folder 
try :
        sys.path.insert(0, working_dir+'/BurnieYilmazRS19/dataPrep/TWITTER/text/' )
        from  twitter_extracting import TextExtractor
except ModuleNotFoundError :
        try: 
                sys.path.insert(0, working_dir+'/crypto_finance_anlysis/BurnieYilmazRS19/dataPrep/TWITTER/text/' )
                from  twitter_extracting import TextExtractor
        except ModuleNotFoundError :
                sys.path.insert(0, working_dir+'/dataPrep/TWITTER/text/' )
                from  twitter_extracting import TextExtractor




def data_extracting(start, end, subreddit, name_for_file_extracting):
    
        
        # #Print current time:
        # print(datetime.now())

        #Sets up extractor object:
        print("start ", start)
        print("end ", end)
        print("subreddit ", subreddit)


        obj = TextExtractor(
                
                start=start, 
                end=end, 
                subreddit=subreddit
                # start=1640023150, 
                # end=1640823600   
         )

        print(obj)

        #Extract data:
        try:
                obj.extract_data()
        except TypeError:
                print("type error in data extracting")
                return('null')

        #Stores collected data in a dataframe:
        data = pd.DataFrame({
                'author': obj.get_authors(),
                'time_stamp': obj.get_time_stamp(),
                'text': obj.get_text()
                })
        print("data")

        #Remove duplicate rows:
        data.drop_duplicates(subset=None, keep='first', inplace=True)



        print("name_for_file_extracting ###", name_for_file_extracting)

        #Store as pickle file:        
        data.to_pickle(name_for_file_extracting)

        #Time range: after and including  1 Jan 2017 (00:00) to before and 
        #not including 4 Dec 2018 (00:00) w times in GMT.
        #The API records time stamp to the second.
