import numpy as np
import pandas as pd

from itertools import chain
from collections import Counter

class vocabCounter(object):
    def __init__(self, rawData, start, end, step):
        self._rawData = rawData
        self._countData = None
        self._vocab = list(set(chain.from_iterable(rawData.text.tolist())))
        self._vocab.sort()
        self._days = range(start, end, step)
        self._start = start
        self._step = step

    def getVocab(self): return(self._vocab)

    def getDays(self): return(np.array(self._days).reshape((-1,1)))

    def getRaw(self): return(self._rawData)

    def getCountData(self): return(self._countData)

    def oneTokenPerSubmission(self): 
        self.getRaw()['text'] = self.getRaw().text.apply(lambda x: list(set(x)))

    def createCountData(self, verbose=True):
        base_count = Counter({token:0 for token in self._vocab})
        # print('base_count')
        # print(base_count)
        
        total_sub_counts = np.array([])

        for i in self._days:
            print('i')
            print(i)
            counter = base_count.copy()
            
            days_data = self._rawData[(self._rawData.time_stamp >= i) & (self._rawData.time_stamp < i + self._step)]
            
            days_text = chain.from_iterable(days_data.text.tolist())
            
            counter.update(days_text)
            
            if i == self._start:
                daily_counts = np.array(list(counter.values())).reshape(1,len(self._vocab))
                total_sub_counts = np.array([len(days_data)])
            else:
                daily_counts = np.append(
                    daily_counts, 
                    np.array(list(counter.values())).reshape(1,len(self._vocab)), 
                    axis = 0)
                total_sub_counts = np.append(total_sub_counts, len(days_data))
            if verbose: print('DATE:', f"{i}....................................", end='\r')

        values = np.concatenate((self.getDays(), total_sub_counts.reshape(-1,1), daily_counts), axis=1)

        self._countData = pd.DataFrame(data=values, columns = np.append('day_time_stamp', np.append('no_submissions', self._vocab)))

    