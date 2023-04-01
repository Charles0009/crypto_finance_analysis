import re, unicodedata, nltk
import pandas as pd
import numpy as np
import string

from nltk.corpus import stopwords
from nltk.stem import SnowballStemmer, WordNetLemmatizer

#Required downloads from nltk: stopwords (supplemented by abbreviations - see line 85) and punkt
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('omw-1.4')

class TextProcessor(object):
    def __init__(self, textSeries):
        self.__textSeries = textSeries

    def processText(self):
        return(self.__textSeries.apply(lambda x: x.lower())
                                .apply(SentenceProcessor.removelongText)
                                .apply(SentenceProcessor.standardiseBitcoin)
                                .apply(SentenceProcessor.removeURL)
                                .apply(SentenceProcessor.removeHTMLCharacterEntities)
                                .apply(SentenceProcessor.removeLineJump)
                                .apply(SentenceProcessor.removeHandle)
                                .apply(SentenceProcessor.removeRemovedDeleted)
                                .apply(SentenceProcessor.removeNonASCII)
                                .apply(SentenceProcessor.removePunctuation)
                                .apply(SentenceProcessor.removeQuotes)
                                .apply(SentenceProcessor.aggregateNumberTypes)
                                .apply(SentenceProcessor.standardiseTransactions)
                                .apply(SentenceProcessor.aggregateLN)
                                .apply(SentenceProcessor.phoneNumber)
                                .apply(nltk.word_tokenize)
                                .apply(TokenProcessor.removeStopwords)
                                .apply(TokenProcessor.lemmatizeAndStem)
                                .apply(TokenProcessor.mineMinerAgg)
                                )
        

class SentenceProcessor(object):

    @staticmethod
    def removelongText(x): return(re.sub(pattern=r"\w{50,}", string=x, repl=''))

    @staticmethod
    def standardiseBitcoin(x): return(re.sub(r"(btc|xbt)\b", " bitcoin ", x))

    @staticmethod
    def removeURL(x): return(re.sub(pattern=r'[(]?http\S+', string= x, repl=''))

    @staticmethod
    def removeHTMLCharacterEntities(x): return(re.sub(pattern=r'&[\w|;|#]+;', string = x, repl = ''))

    @staticmethod
    def removeLineJump(x): return(x.replace("\n", " "))

    @staticmethod
    def removeHandle(x): return(re.sub(pattern=r'(\S+)?@\S+|\/[u|r]\/\S+', string= x, repl=''))
     
    @staticmethod
    def removeRemovedDeleted(x): return(x.replace('[removed]', '').replace('[deleted]', ''))

    @staticmethod
    def removeNonASCII(x): return(unicodedata.normalize('NFKD', x).encode('ascii', 'ignore').decode('utf-8', 'ignore'))

    @staticmethod
    def removePunctuation(x): 
        """
        This removes all punctuation except: $ sign kept to indicate an amount of money; and ' kept as it is used in abbreviations
        """
        return(re.sub("[!\"#%&()*+,-./:;<=>?@[\]^_`{|}~]+", "", x).replace("\\", ""))

    @staticmethod
    def removeQuotes(x): 
        """
        This removes quotes around but not in the middle of words.
        """        
        return(re.sub(r"^'|(?<=\s)'|'(?=\s|$)", "", x))
    
    @staticmethod
    def aggregateNumberTypes(x): return(re.sub(r"(usd|\$|(us )?dollar(s)?)", " dollar_marker_symbol ", x))

    @staticmethod
    def standardiseTransactions(x):
        return(re.sub(r"\b(tx)\b", "transaction", x))
        
    @staticmethod
    #def aggregateLN(x): return(re.sub(r"(?<=\s)(ln|(lightning network)(s)?)(?=\s)", "LN", x))
    def aggregateLN(x): return(re.sub(r"\b(ln|(lightning network)(s)?)\b", "ln", x))        

    @staticmethod
    def phoneNumber(x): return(re.sub(r"(tele)?phone number", "phone_number", x))


class TokenProcessor(object):
  
    @staticmethod
    def removeStopwords(x):
        return([newToken for newToken in x if SentenceProcessor.removeQuotes(newToken) not in TokenProcessor.__getStopwords()])

    @staticmethod
    def lemmatizeAndStem(x):
        return([SnowballStemmer("english").stem(WordNetLemmatizer().lemmatize(newToken,pos='v')) for newToken in x if x != 'dollar_marker_symbol'])

    @staticmethod
    def mineMinerAgg(x): 
        def mineMiner(x):
            if x == "miner": return('mine')
            else: return(x)
        return([mineMiner(newToken) for newToken in x])

    @staticmethod
    def __getStopwords():
        return(stopwords.words('english') + [ "n't"])

