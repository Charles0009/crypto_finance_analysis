import datetime
import json
import time
import requests
from urllib.request import urlopen
from urllib.error import HTTPError
import pandas as pd
import time


class TextExtractor(object):

    def __init__(self, start, end, subreddit):
        self.__start = start
        self.__end = end
        self.__subreddit = subreddit
        self.__data = None
        pass

    def extract_data(self):

        updatedStart = self.__start
        print(datetime.datetime.fromtimestamp(updatedStart))
        print(datetime.datetime.fromtimestamp(self.__end))
        AllData = []
        count = 0

        while True:
            data_list = self.__jsonExtractor(
                start=updatedStart, end=self.__end)
            if len(data_list["data"]) > 1:
                AllData.extend(data_list["data"])
                updatedStart = data_list["data"][-1]["created_utc"] - 1
                tracker = (updatedStart-self.__start) / \
                    (self.__end-self.__start) * 100
                print(datetime.datetime.fromtimestamp(updatedStart))

                print(len(AllData))
                print(
                    f"{tracker} per completed...........................", end='\r')
                count += 1
                print(count)
            else:
                break

        print(count)
        self.__data = AllData
        pass

    def get_data(self): return(self.__data)

    def get_authors(self):
        return(list(map(lambda x: x['author'], self.__data)))

    def get_time_stamp(self):
        return(list(map(lambda x: x['created_utc'], self.__data)))

    def get_text(self):
        return(list(map(self.__textMerging, self.__data)))

    def __jsonExtractor(self, start, end):

        try:
            with urlopen(f"https://api.pushshift.io/reddit/search/submission/?subreddit={self.__subreddit}&size=100&sort_type=created_utc&sort=asc&fields=author,title,selftext,created_utc&before={end}&after={start}") as url:
                element = json.loads(url.read().decode())
                return(element)
        except HTTPError as e:
            print('error', e)
            if (e.code == 521):
                print(
                    "\n \n \n \n The api may be down, check the following website : https://api.pushshift.io/ \n \n\n \n")
            if (e.code == 429):
                time.sleep(61)
                try:
                    return(self.__jsonExtractor(start=start, end=end))
                except HTTPError:
                    print('failed twice')

    def __textMerging(self, x): return(self.__textMergingSubmission(x))

    def __textMergingSubmission(self, x):
        try:
            return(x['title'] + '. ' + x['selftext'])
        except KeyError:
            return(x['title'])
