# ----------------------------------------------------------------------------------
# # Extracting Reddit data from Pushshift API
# ----------------------------------------------------------------------------------


from  BurnieYilmazRS19.dataPrep.REDDIT.text.extracting import TextExtractor
import pandas as pd
import json
import datetime 

def data_extracting(start, end, subreddit, name_for_file_extracting):
    
        
        # #Print current time:
        # print(datetime.now())

        #Sets up extractor object:
        obj = TextExtractor(
                
                start=start, 
                end=end, 
                subreddit=subreddit
                # start=1640023150, 
                # end=1640823600   
         )

        #Extract data:
        try:
                obj.extract_data()
        except TypeError:
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



        print(name_for_file_extracting)

        #Store as pickle file:        
        data.to_pickle(name_for_file_extracting)

        #Time range: after and including  1 Jan 2017 (00:00) to before and 
        #not including 4 Dec 2018 (00:00) w times in GMT.
        #The API records time stamp to the second.
