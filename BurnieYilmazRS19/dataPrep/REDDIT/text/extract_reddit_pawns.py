import pandas as pd
from pmaw import PushshiftAPI
api = PushshiftAPI()
import datetime as dt
before = int(dt.datetime(2022,8,1,0,0).timestamp())
after = int(dt.datetime(2022,4,1,0,0).timestamp())


# subreddit="btc"
# limit=100
# comments = api.search_comments(subreddit=subreddit, limit=limit, before=before, after=after)
# print(f'Retrieved {len(comments)} comments from Pushshift')


posts = api.search_submissions(subreddit="science", limit=1000)
print(f'Retrieved {len(posts)} comments from Pushshift')
# comment_list = [comment for comment in comments]
comments_df = pd.DataFrame(posts)
# preview the comments data
comments_df.head(5)
