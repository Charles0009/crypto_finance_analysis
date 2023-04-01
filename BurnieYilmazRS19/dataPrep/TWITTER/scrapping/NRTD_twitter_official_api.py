import json
import time
import tweepy
import pandas as pd
import requests
import numpy as np

from dateutil import parser

# API keyws that yous saved earlier
api_key = "SPwY1EBmWAXvORRh3EzTPvkzh"
api_secrets = "EUA0jsIzbas9afL07XV1MCWedZeUfEsavVSt0omn1VKncciU4W"
access_token = "1325801213431050241-7TJ2ts9Xlvx9a18oAOENA0bYUteRFn"
access_secret = "XaKcYbdrL0Su8KAFAsGUzCiGVat2CQ8MnL4gXLlbYzU4B"
bearer_token = "AAAAAAAAAAAAAAAAAAAAAHiDkgEAAAAAclqEjVRDRJcveZ8yCYM7gao3aE0%3DwJzfxyaJ6OzoxCor3obBRITVjGwrIfmtAk4KRnrwYqf1Ay5KED"

# Authenticate to Twitter
auth = tweepy.OAuthHandler(api_key,api_secrets)
auth.set_access_token(access_token,access_secret)
 
api = tweepy.API(auth)
client = tweepy.Client(bearer_token)
 
try:
    api.verify_credentials()
    print('Successful Authentication')
except:
    print('Failed authentication')



# fetching the user
user = api.get_user(screen_name='elonmusk')
# fetching the followers_count
followers_count = user.followers_count
print("The number of followers of the user are : " + str(followers_count))




# # We create a tweet list as follows:
tweets = api.user_timeline(screen_name="elonmusk", count=200)
print("Number of tweets extracted: {}.\n".format(len(tweets)))

# We create a pandas dataframe as follows:
data = pd.DataFrame(data=[tweet.text for tweet in tweets], columns=['Tweets'])
    
# We display the first 10 elements of the dataframe:
# # print(dir(tweets[0]))
data['author']  = np.array([tweet.author.screen_name for tweet in tweets])
data['language']  = np.array([tweet.lang for tweet in tweets])
data['len']  = np.array([len(tweet.text) for tweet in tweets])
data['ID']   = np.array([tweet.id for tweet in tweets])
data['Date'] = np.array([tweet.created_at for tweet in tweets])
data['Source'] = np.array([tweet.source for tweet in tweets])
data['Likes']  = np.array([tweet.favorite_count for tweet in tweets])
data['RTs']    = np.array([tweet.retweet_count for tweet in tweets])
data['Date'] = data['Date'].apply(lambda x: parser.parse(str(x)).timestamp())

print(data.head(4))


print(user_followers)
print(user_follows)
