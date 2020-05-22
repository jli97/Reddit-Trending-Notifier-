import praw
import math
import time
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
class Data:
    reddit = praw.Reddit(client_id = 'aM_mGMSXor7avg',client_secret = '	rlfl7DoUGE74y_5UlcP2jLntoVw', username='PRAW_97', password='123456789j', user_agent='Better Trending')
    
    def __init__(self, sub_name):
        self.sub_name = sub_name
        self.subreddit = self.reddit.subreddit(sub_name)
        self.new_posts = self.getNewPosts() # Only look at posts posted within 24hrs
        self.model = self.regression() 

    def getSTD(sub_name):
    mean = getAverageUpVotes(sub_name)

    sum = 0
    count = 0
    for submission in subreddit.hot(limit=50):
        sum = pow((sum + (submission.score - mean)), 2)
        count = count + 1

    sum = sum/(count - 1)
    std = sqrt(sum)

    return std

    def getNewPosts(self):
        ret = []
        for submission in self.subreddit.hot(limit=50):
            date_created = submission.created_utc # Unix Time
            date_today = time.time() 

            if((date_today - date_created) > (24*60*60)): # Post is less than 24hrs old
                ret.insert(submission)
        
        return ret
    
    def regression(self): # Returns LinearRegression Object with score as dependent and num_comment, pos_age as independent
        #Get Data
        upvotes = [] 
        num_comment = [] 
        post_age = [] 

        for submission in self.subreddit.hot(limit=50):
            upvotes.insert(submission.score)
            num_comment.insert(submission.num_comments)
            post_age.insert(submission.created_utc - time.time())
        
        independent = {'num_comment': num_comment, 'post_age': post_age}
        dependent = {'upvotes': upvotes}
        x = pd.DataFrame(data=independent)
        y = pd.DataFrame(data=dependent)
        #Regression
        lr = LinearRegression(fit_intercept=False)
        lr.fit(x,y)

        return lr