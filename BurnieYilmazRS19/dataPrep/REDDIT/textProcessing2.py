# ----------------------------------------------------------------------------------
# # Processing Reddit Data
# ----------------------------------------------------------------------------------

import os
import sys

working_dir = str(os.getcwd())

# Insert the path of modules folder 
sys.path.insert(0, working_dir+'/BurnieYilmazRS19/dataPrep/REDDIT/text/' )


from  processing import TextProcessor
from  dataHandling import DataHandling

from datetime import datetime
from concurrent.futures import ProcessPoolExecutor
from multiprocessing import freeze_support

import pandas as pd

def termProcessor(data): return(TextProcessor(data.text).processText())

#below takes about half an hour to run.
def textprocess(name_for_file_extracting):
        
        freeze_support()


        print("Submissions data loaded - ", datetime.now())
        #print(pd.read_pickle('/mnt/c/Users/charl/Desktop/finance_perso/BurnieYilmazRS19/dataPrep/REDDIT/data/extracting/submissions_041218.pkl'))
        dataObj = DataHandling(data_frame = pd.read_pickle(name_for_file_extracting))
        dataObj.removeExcludedRows()
        dataObj.splitData(step=10000)
        
        print("Begin TERMS data processing - ", datetime.now())
        with ProcessPoolExecutor() as executor:
                newTextList = executor.map(termProcessor, dataObj.getDataList(), chunksize = 3)
        # for r in newTextList:
        #         print(r)

        print("Begin TERMS data storing - ", datetime.now())        
        for i, text in enumerate(newTextList):
                dataObj.getDataList()[i]['text'] = text
        
        print("Output TERMS data")

        print(dataObj.getDataList())

        dataObj.outputDataFrames(folder = 'terms', label = 'subTerms_tests')

# textprocess()
