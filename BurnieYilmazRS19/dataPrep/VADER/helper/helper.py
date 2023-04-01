import re
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer as SIA
nltk.downloader.download('vader_lexicon')


class helper(object):

    @staticmethod
    def sentimentLabeller(compound):
        if compound < -0.2: return("NEG")
        if compound < 0.2: return("NEU")
        return("POS")

    @staticmethod
    def sentimentProcessor(submission_text):
        sia = SIA()
        compound = sia.polarity_scores(submission_text)['compound']
        return(helper.sentimentLabeller(compound))

    @staticmethod
    def labelCounter(data,i):
        countsData = dict()

        VADER = data[(data.time_stamp >= i) & (data.time_stamp < i + 86400)].VADER

        countsData['EpochDate'] = i
        countsData['NEG'] = (VADER == 'NEG').sum()
        countsData['NEU'] = (VADER == 'NEU').sum()
        countsData['POS'] = (VADER == 'POS').sum()
        countsData['no_submissions'] = len(VADER)

        return(countsData)
    
    @staticmethod
    def submission_filterer(submission_text, term=False):
        if term in ["tax"]:
            if re.search(r"(\b)(tax|taxes|taxed|taxing)(\b)",  submission_text): return(True)
        if term in ["ban"]: 
            if re.search(r"(\b)(ban|bans|banned|banning)(\b)",  submission_text): return(True)
        if term == "DMS":
            if re.search(r"(usd|\$|(us )?dollar(s)?)",  submission_text): return(True)
        if term == "bitcoin":
            if re.search(r"(\b)(bitcoin|bitcoins|btc|xbt)\b",  submission_text): return(True)
        else :
            if re.search(term,  submission_text): return(True)
        return(False)

    @staticmethod
    def categoriser(submission_text, filterer, processor, term=False):
        if filterer(submission_text, term=term):
            return(processor(submission_text))
        else:
            return("")

    @staticmethod
    def labelCounterTerms(compressed_data,i):
        data = compressed_data[0]
        liste_of_words = compressed_data[1]

        countsData = dict()

        countsData['EpochDate'] = i

        # print("\n \n data !!!!!!!!!!!!!!!! ", type(data))
        # # print("\n \n  liste of _words  : ", liste_of_words)
        # print("\n \n  iiiiiiiiiiiiiiiiiiii  : ", type(i)) 

        data2 = data[(data.time_stamp >= i) & (data.time_stamp < i + 86400)]

        countsData['no_submissions'] = len(data2)

        # for word in ["tax", "ban", "DMS", "bitcoin"]:  
        for term in liste_of_words:  
            # print("term ::::::::::::::::::::::::::::::::::::::::: ", term)
            countsData[f'{term}_NEG'] = (data2[f'{term}_VADER'] == 'NEG').sum()
            countsData[f'{term}_NEU'] = (data2[f'{term}_VADER'] == 'NEU').sum()
            countsData[f'{term}_POS'] = (data2[f'{term}_VADER'] == 'POS').sum()     
        
        # print(" \n couuuuuuuuuuuuuuuuuuuuuuuuuunt data ")
        # print(countsData)

        return(countsData)