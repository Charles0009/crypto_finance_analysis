import pandas as pd
import numpy as np
import string
import os
import re

class DataHandling(object):
    """
    This class is responsbile for reading, filtering and writing to memory one or more dataframes in a list.
    """

    def __init__(self, data_frame=pd.DataFrame()):
        """
        Can initialise with dataframe(s)
        """
        if data_frame.empty:
            self.__dataList = []
        else:           
            self.__dataList = [data_frame]

    def collectData(self, dataPath, regexpr, verbose=True):
        """
        Can collect data from a given path to a folder
        """
        self.__dataList = []
        submissionFiles = []
        for dataFile in os.listdir(dataPath):
            if (re.search(regexpr, dataFile)): submissionFiles.append(dataFile)

        noFiles = len(submissionFiles)
        
        for i, datafile in enumerate(submissionFiles):
            self.__dataList.append(pd.read_pickle(dataPath + datafile))
            if verbose: print(f"{(i + 1) / noFiles * 100} per completed...........................", end='\r')
            
        if verbose: print("100 per completed...........................")

    #Reader Functions

    def getDataList(self): return(self.__dataList)

    def selectFirstFrame(self):
        if len(self.__dataList) > 1:
            raise Exception("stopped as more than one dataset")
        else:
            return(self.__dataList[0])

    #Filter Functions

    def removeExcludedRows(self):
        data = self.selectFirstFrame()

        #Removing rows pre-emptively
        ####Moderator, crypto_bot and duplicate text:
        data = data[data.author != 'rBitcoinMod']
        data = data[data.author != 'crypto_bot']
        data = data.drop_duplicates('text')
        ####Row is just [deleted] or [removed], or is blank:
        data = data[~data.text.isin(['[deleted]', '[removed]'])]
        data = data[data.text != '']

        #Resetting index after above changes:
        data.reset_index(drop=True, inplace=True)

        self.__dataList = [data]

    #Convert from one to many and vice-versa:

    def splitData(self, step= 300000):
        """
        Splits one dataframe into many according to a step
        """
        data = self.selectFirstFrame()
        data_list = []
        for i in range(0, len(data), step):
            if i + step-1 < len(data): 
                data_list.append(data.loc[i:(i+step-1)].reset_index(drop=True))
            else:
                data_list.append(data.loc[i::].reset_index(drop=True))

        self.__dataList = data_list

    def aggData(self):
        """
        Concatenates all dataframes into one
        """
        submissions = pd.concat(self.__dataList)
        self.__dataList = [submissions.sort_values('time_stamp').reset_index(drop=True)]

    def outputDataFrames(self, folder, label):
        current_directory = str(os.getcwd())

        for i, df in enumerate(self.__dataList):


            #path_for_file = current_directory+"/BurnieYilmazRS19/dataPrep/REDDIT/data/processing/{folder}/{label}_{i}.pkl{folder}/{label}_{i}.pkl"
            exec(f'df.to_pickle("{current_directory}/BurnieYilmazRS19/dataPrep/REDDIT/data/processing/{folder}/{label}_{i}.pkl")')