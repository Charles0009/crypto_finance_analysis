import os
import sys
import datetime






def extract_full_reddit_token_frequency(start_epoch, end_epoch, subreddit):
    working_dir = str(os.getcwd())
    print("working_dir", working_dir)
    try : 
    # Insert the path of modules folder 
        sys.path.insert(0, working_dir+'/BurnieYilmazRS19/dataPrep/TWITTER/' )
        from  twitter_dataExtracting1 import data_extracting
        from twitter_textProcessing2 import textprocess
        from  twitter_dailyWordFreq3 import dailywordfreq

    except ModuleNotFoundError :
        sys.path.insert(0, working_dir+'/crypto_finance_anlysis/BurnieYilmazRS19/dataPrep/TWITTER/' )
        from  twitter_dataExtracting1 import data_extracting
        from twitter_textProcessing2 import textprocess
        from  twitter_dailyWordFreq3 import dailywordfreq



   
    start_in_date = datetime.datetime.fromtimestamp(start_epoch)
    end_in_date = datetime.datetime.fromtimestamp(end_epoch)
    print(" start date : " + str(start_in_date))
    print(" start date : " + str(end_in_date))


    start_in_date = str(start_in_date)
    end_in_date = str(end_in_date)
    start_in_date = start_in_date[:10]
    end_in_date = end_in_date[:10]

    current_directory = str(os.getcwd())

    name_for_file ='twitter_'+subreddit+"_"+start_in_date+"_"+end_in_date
    try : 
        print("data extracting 2")
        name_for_file_extracting = current_directory+'/BurnieYilmazRS19/dataPrep/TWITTER/data/twitter_extracting/'+name_for_file+'.pkl'
         #call to the api for extraction
        print("name_for_file_extracting ",name_for_file_extracting)
        data_extracting( start=start_epoch, 
                        end=end_epoch ,
                        subreddit=subreddit,
                        name_for_file_extracting = name_for_file_extracting )
        #call to the api for extraction
        print("text processing 2")
        textprocess(name_for_file_extracting)
    except FileNotFoundError:
        try: 
            print("data extracting 4")
            name_for_file_extracting = current_directory+'/dataPrep/TWITTER/data/twitter_extracting/'+name_for_file+'.pkl'
            print("name_for_file_extracting ",name_for_file_extracting)
            #call to the api for extraction
            data_extracting( start=start_epoch, 
                            end=end_epoch ,
                            subreddit=subreddit,
                            name_for_file_extracting = name_for_file_extracting )
            #call to the api for extraction
            print("text processing 4")
            textprocess(name_for_file_extracting)
            
        except FileNotFoundError:            
            print("data extracting 3")
            name_for_file_extracting = current_directory+'/crypto_finance_anlysis/BurnieYilmazRS19/dataPrep/TWITTER/data/twitter_extracting/'+name_for_file+'.pkl'
            #call to the api for extraction
            data_extracting( start=start_epoch, 
                            end=end_epoch ,
                            subreddit=subreddit,
                            name_for_file_extracting = name_for_file_extracting )
            #call to the api for extraction
            print("text processing 3")
            textprocess(name_for_file_extracting)



    print("name for file extracting : " + name_for_file_extracting)
    try : 
        name_for_saving_processed = current_directory+'/BurnieYilmazRS19/dataPrep/TWITTER/data/twitter_processing/twitter_tokenFreq/'+name_for_file+'.pkl'
        
        print("name for file processing : " + name_for_saving_processed)

    
        print("daily word frequency")
        dailywordfreq( start=start_epoch, 
                        end=end_epoch, 
                        name_for_saving_processed = name_for_saving_processed   )

        print("name for save file : " + name_for_saving_processed)
    except FileNotFoundError:
        try:
            name_for_saving_processed = current_directory+'/crypto_finance_anlysis/BurnieYilmazRS19/dataPrep/TWITTER/data/twitter_processing/twitter_tokenFreq/'+name_for_file+'.pkl'
            
            print("name for file processing : " + name_for_saving_processed)

        
            print("daily word frequency")
            dailywordfreq( start=start_epoch, 
                            end=end_epoch, 
                            name_for_saving_processed = name_for_saving_processed   )

            print("name for save file : " + name_for_saving_processed)

        except FileNotFoundError:
            name_for_saving_processed = current_directory+'/dataPrep/TWITTER/data/twitter_processing/twitter_tokenFreq/'+name_for_file+'.pkl'
        
            print("name for file processing : " + name_for_saving_processed)

        
            print("daily word frequency")
            dailywordfreq( start=start_epoch, 
                            end=end_epoch, 
                            name_for_saving_processed = name_for_saving_processed   )

            print("name for save file : " + name_for_saving_processed)


    return(name_for_saving_processed)

# start_epoch = 1648771200
# end_epoch =   1659312000
# subreddit= 'CryptoCurrency'
# extract_full_reddit_token_frequency(start_epoch, end_epoch, subreddit)