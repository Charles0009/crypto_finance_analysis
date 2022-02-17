# ----------------------------------------------------------------------------------
# # Script for Finding Chain of Associated Words
# ----------------------------------------------------------------------------------

import pandas as pd 
import argparse

from dataPrep.REDDIT.text.dataHandling import DataHandling
from dataPrep.REDDIT.text.vocabCounter import vocabCounter

print("Collecting Data")
dataObj = DataHandling()
dataObj.collectData(dataPath='/mnt/c/Users/charl/Desktop/finance_perso/BurnieYilmazRS19/dataPrep/REDDIT/data/processing/terms/', regexpr=r'^subTerms', verbose=True)
dataObj.aggData()

termsData = dataObj.selectFirstFrame()

del dataObj

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--term', default = "['tax']")
    parser.add_argument('--data', default = 'p1')
    parser.add_argument('--number', default = '20')
    terms = eval(parser.parse_args().term)
    data = parser.parse_args().data
    number = parser.parse_args().number

    print("FILTER DATA")

    for term in terms:
        termsData = termsData[termsData.text.apply(lambda x: term in x)]

    if data == 'p1': start, end = 1483228800, 1513382400
    if data == 'p2': start, end = 1513382400, 1530230400
    if data == 'p3': start, end = 1530230400, 1542240000
    if data == 'all': start, end = 1483228800, 1543881600

    print("CREATE VOCAB")
    
    vc = vocabCounter(
    rawData = termsData,
    start = start,
    end = end,
    step = 86400
    )

    vc.oneTokenPerSubmission()

    vc.createCountData()

    counts = vc.getCountData()

    del counts['day_time_stamp']
    del counts['no_submissions']

    print("                                                                   ", end="\r")

    counts = counts.sum(axis=0)

    print((counts/counts[terms[0]]*100).sort_values(ascending=False).head(eval(number)).to_latex())
    
    #print((counts/counts[terms[0]]*100).sort_values(ascending=False).head(eval(number)))

    



    





