import pandas as pd
from datetime import datetime
from concurrent.futures import ProcessPoolExecutor
from multiprocessing import freeze_support
from functools import partial

from helper.helper import helper

import sys
sys.path.append('../REDDIT/')

from text.processing import SentenceProcessor
from text.dataHandling import DataHandling



from nltk.sentiment.vader import SentimentIntensityAnalyzer as SIA


def termProcessor(term=False,data=None): 
    return(
        data.text.apply(lambda x: x.lower())
            .apply(SentenceProcessor.removelongText)
            .apply(SentenceProcessor.removeURL)
            .apply(SentenceProcessor.removeHTMLCharacterEntities)
            .apply(SentenceProcessor.removeLineJump)
            .apply(SentenceProcessor.removeRemovedDeleted)
            .apply(SentenceProcessor.standardiseTransactions)
            .apply(lambda x: helper.categoriser(submission_text=x, filterer=helper.submission_filterer, processor=helper.sentimentProcessor, term=term))
    )


if __name__ == '__main__':
    freeze_support()
    

    print("Submissions data loaded - ", datetime.now())
    dataObj = DataHandling(data_frame = pd.read_pickle('../REDDIT/data/extracting/submissions_041218.pkl'))
    dataObj.removeExcludedRows()
    dataObj.splitData(step=10000)

    for word in ["tax", "ban", "DMS", "bitcoin"]:

        print(word)
        termProcessor2 = partial(termProcessor, word)  

        print("Begin data processing - ", datetime.now())
        with ProcessPoolExecutor() as executor:
            textList = executor.map(termProcessor2, dataObj.getDataList(), chunksize = 3)
            
        print("Begin data storing - ", datetime.now())        
        for i, text in enumerate(textList):
            dataObj.getDataList()[i][f'{word}_VADER'] = text
            
        del textList

    dataObj.aggData()

    data = dataObj.selectFirstFrame()

    del dataObj

    print("REMOVE SUBMISSIONS BLANK AFTER PROCESSING")
    data = data[data.text.apply(lambda x: x != [])]

    sentimentData = pd.DataFrame()

    EpochDate_list = []
    no_submissions_list = []

    for word in ["tax", "ban", "DMS", "bitcoin"]:
        exec(f"{word}_NEG_list = []")
        exec(f"{word}_NEU_list = []")
        exec(f"{word}_POS_list = []")

    
    print("Counting labels for each term")       

    labelCounter2 = partial(helper.labelCounterTerms,data)

    with ProcessPoolExecutor() as executor:
        sentiments = executor.map(labelCounter2, list(range(1483228800, 1543881600, 86400)), chunksize = 10)

    for i in sentiments:
        EpochDate_list.append(i['EpochDate'])
        no_submissions_list.append(i['no_submissions'])
        for word in ["tax", "ban", "DMS", "bitcoin"]:
            exec(f"{word}_NEG_list.append(i['{word}_NEG'])")
            exec(f"{word}_NEU_list.append(i['{word}_NEU'])")
            exec(f"{word}_POS_list.append(i['{word}_POS'])")
        
    sentimentData['EpochDate'] = EpochDate_list
    sentimentData['no_submissions'] = no_submissions_list

    for word in ["tax", "ban", "DMS", "bitcoin"]:          
        exec(f"sentimentData['{word}_NEG'] = {word}_NEG_list")
        exec(f"sentimentData['{word}_NEU'] = {word}_NEU_list")
        exec(f"sentimentData['{word}_POS'] = {word}_POS_list")
    

    sentimentData.to_csv('VADER.csv')

