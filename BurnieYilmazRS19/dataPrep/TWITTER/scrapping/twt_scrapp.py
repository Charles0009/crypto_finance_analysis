import twint
import numpy as np

def call_for_tweeter(account, limit, min_likes):
    # Configure
    c = twint.Config()
    #c.Search = ['BTC']
    c.Username = account
    c.Limit = limit
    c.User_full = True
    c.Pandas = True
    c.Min_likes = min_likes
    # Run
    twint.run.Search(c)
    Tweets_df = twint.storage.panda.Tweets_df
    if not Tweets_df.empty:
        Tweets_df = Tweets_df.drop(['id', 'conversation_id', 'created_at','timezone','place', 'language','user_id', 'user_id_str',  'username', 'name','day', 'hour','link', 'urls', 'photos', 'video','thumbnail', 'retweet'], axis=1)
        Tweets_df = Tweets_df.iloc[: , :-12]
        
    return(Tweets_df)
    

def get_nb_followers(account):
     #Configure
    t = twint.Config()
    t.Username = account
    t.Pandas = True
    twint.run.Lookup(t)
    follow_df = twint.storage.panda.User_df
    nb_followers = follow_df['followers']
    nb_followers = nb_followers.iloc[0]
    return (nb_followers)

def rearrange_string(line):
        sliced = line[20:]
        sliced = sliced[:sliced.index("/")]        
        return(sliced)

def get_name_for_url_quotes(df_twts):
    #### getting the column for quote_url 
    column_for_quote_url = df_twts.iloc[:,-1:]
    column_for_quote_url = column_for_quote_url['quote_url'].values 
    filter_object = filter(lambda x: x != "", column_for_quote_url)
    without_empty_strings = list(filter_object)
    final_list = list(map(rearrange_string, without_empty_strings))
    final_list = list(set(final_list))
    return(final_list)


# test2 = call_for_tweeter('elonmusk', 100, 100)
# # test = get_nb_followers('parabolic_matt')
# print(test2)


# Configure
c = twint.Config()
c.Username = "elonmusk"
c.Search = "great"

# Run
twint.run.Search(c)