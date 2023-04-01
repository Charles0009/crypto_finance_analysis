# ----------------------------------------------------------------------------------
# # Script for tracking word frequency over time
# ----------------------------------------------------------------------------------


import pandas as pd
import argparse
import time
import matplotlib.pyplot as plt
import matplotlib.dates as mdate
import numpy as np
import re
import os 
import sys
working_dir = str(os.getcwd())
print(working_dir)

class TrendDrawer(object):
    def __init__(self,data,word, date_range, plt):
        self.plt = plt
        self.data = data
        self.word = word
        self.time = mdate.epoch2num(data['day_time_stamp'])
        self.date_range = date_range
        self.title = parser.parse_args().title
        self.__setUp()

    def __setUp(self):
        self.plt.figure(figsize = (20,20))
        _, ax = plt.subplots()
        ax.xaxis.set_major_formatter(mdate.DateFormatter("%b-%y"))
        ax.xaxis.set_major_locator( mdate.MonthLocator())
        if parser.parse_args().proportion == 'end': plt.axhline(y=100, linestyle = '-', color='gray')

    def plot_word(self):
        self.plt.plot_date(self.time, self.data[self.word], linestyle = '-', color = 'k' )
        # self.plt.plot_date(self.time, self.data[self.word], linestyle = '-', marker='', color = 'k' )
        self.__style_axes()

    def __style_axes(self):
        self.plt.title(self.title) 
        # self.plt.xlim(date_range[0], date_range[1])
        self.plt.xticks(rotation=45)
        # self.plt.axvline(x="16 Dec 2017", linestyle = '--', color='k')
        # self.plt.axvline(x="29 June 2018", linestyle = '--', color='k')
        # self.plt.axvline(x="15 Nov 2018", linestyle = '--', color='k')

    def save_fig(self):
        self.plt.tight_layout()
        if window == 1:
            self.plt.savefig(working_dir + '/BurnieYilmazRS19/visuals/termTracker/' + self.word + "22.jpeg")
        else:
            self.plt.savefig(working_dir + '/BurnieYilmazRS19/visuals/termTracker/' + self.word + "_" + str(window) + "22.jpeg") 
            

if __name__ == "__main__":
     parser = argparse.ArgumentParser()
     parser.add_argument('--term', default = 'bitcoin')
     parser.add_argument('--start', default = "Apr 22")
     parser.add_argument('--end', default = 'Jun 22')
     parser.add_argument('--proportion', default = 'submissions')
     parser.add_argument('--title', default = '')
     parser.add_argument('--rolling', default = '1')

     args = parser.parse_args()
     term_tracked = parser.parse_args().term
     date_range = [parser.parse_args().start, parser.parse_args().end]
     window = eval(parser.parse_args().rolling)

     wordFreq = pd.read_pickle(working_dir + '/BurnieYilmazRS19/dataPrep/REDDIT/data/processing/tokenFreq/CryptoCurrencies_2022-04-17_2022-06-17.pkl')

     if parser.parse_args().proportion == 'submissions': wordFreq[term_tracked] = (wordFreq[term_tracked].rolling(window).sum()) / (wordFreq["no_submissions"].rolling(window).sum()) * 100

     if parser.parse_args().proportion == 'end': wordFreq[term_tracked] = wordFreq[term_tracked] / wordFreq[term_tracked].tail(1).tolist()[0] * 100

     print(wordFreq)
     obj = TrendDrawer(data=wordFreq,word=term_tracked,date_range=date_range,plt=plt)
     obj.plot_word()
     obj.save_fig()
     
     




 
    



