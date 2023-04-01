# ----------------------------------------------------------------------------------
# # Calculating Word Frequencies
# ----------------------------------------------------------------------------------

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

import os
import sys

working_dir = str(os.getcwd())
try :
    # Insert the path of modules folder 
    sys.path.insert(0, working_dir+'/BurnieYilmazRS19/dataPrep/TWITTER/text/' )
    from  twitter_dataHandling import DataHandling
    from  twitter_vocabCounter import vocabCounter
except ModuleNotFoundError :
    sys.path.insert(0, working_dir+'/crypto_finance_anlysis/BurnieYilmazRS19/dataPrep/TWITTER/text/' )
    from  twitter_dataHandling import DataHandling
    from  twitter_vocabCounter import vocabCounter



from collections import Counter
from itertools import chain

def dailywordfreq(start, end, name_for_saving_processed):
    

    print("Collecting Data")
    dataObj = DataHandling()
    current_directory = str(os.getcwd())

    try:
        dataObj.collectData(dataPath=current_directory+"/BurnieYilmazRS19/dataPrep/TWITTER/data/twitter_processing/twitter_terms/", regexpr=r'^subTerms', verbose=True)
    except:
        dataObj.collectData(dataPath=current_directory+"/crypto_finance_anlysis/BurnieYilmazRS19/dataPrep/TWITTER/data/twitter_processing/twitter_terms/", regexpr=r'^subTerms', verbose=True)

    
    dataObj.aggData()

    data = dataObj.selectFirstFrame()

    del dataObj

    print("REMOVE SUBMISSIONS BLANK AFTER PROCESSING")

    data = data[data.text.apply(lambda x: x != [])]

    print("CREATE VOCAB")
    vc = vocabCounter(
        rawData = data,
        start = start,
        end = end,
        # start=1640023150, 
        # end=1640823600,
        step = 86400
        )

    #vc.getRaw().to_csv('/mnt/c/Users/charl/Desktop/finance_perso/BurnieYilmazRS19/dataPrep/TWITTER/data/processing/tokenFreq/daily8888.csv')


    del data

    print("AT MOST ONE TERM / SUBMISSION")

    vc.oneTokenPerSubmission()

    print(vc.getRaw())

    print("CREATE COUNTER OBJECT")

    

    vc.createCountData()

    dataf = vc.getCountData()
    dataf.to_pickle(name_for_saving_processed)

#     df2 = pd.read_pickle('/mnt/c/Users/charl/Desktop/finance_perso/BurnieYilmazRS19/dataPrep/TWITTER/data/processing/tokenFreq/dailyTokenFreq_041218.pkl')

#     df2.to_csv('/mnt/c/Users/charl/Desktop/finance_perso/BurnieYilmazRS19/dataPrep/TWITTER/data/processing/tokenFreq/dailyTokenFreq_0666.csv')
