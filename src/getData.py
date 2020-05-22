import praw
import math
import time
import pandas as pd
from sklearn.linear_model import LinearRegression

class Data:
    reddit = praw.Reddit(client_id = 'aM_mGMSXor7avg',client_secret = 'rlfl7DoUGE74y_5UlcP2jLntoVw', username='PRAW_97', password='123456789j', user_agent='Better Trending')
    
    def __init__(self, sub_name):
        self.sub_name = sub_name
        self.subreddit = self.reddit.subreddit(sub_name)
        self.new_posts = self.getNewPosts() # Posts within 24 hours
        self.data_frame = self.getRegressionDf()
        self.lr_obj = self.regression()


    def getNewPosts(self):
        ret = []
        for submission in self.subreddit.hot(limit=50):
            date_created = submission.created_utc # Unix Time
            date_today = time.time() 

            if((date_today - date_created) < (24*60*60) and not (submission.stickied)): # Post is less than 24hrs old
                ret.append(submission)

        return ret
    
    def getRegressionDf(self): # Returns dataframe
        #Get Data
        upvotes = [] 
        post_age = [] 

        for submission in self.subreddit.hot(limit=25): #First page
            if submission.stickied:
                continue
            upvotes.append(submission.score)
            post_age.append(time.time() - submission.created_utc)
        
        independent = {'post_age': post_age}
        ret = pd.DataFrame(data=independent)
        ret['upvotes'] = upvotes
        return ret
    
    def regression(self): # Returns LinearRegression Object with score as dependent and num_comment, pos_age as independent

        x = self.data_frame.iloc[:,0].copy()
        y = self.data_frame.iloc[:,1].copy()

        x = x.values.reshape(-1,1)
        y= y.values.reshape(-1,1)
        #Regression
        lr = LinearRegression(fit_intercept=False) # If post age is 0, upvotes should be 0
        lr.fit(x,y)

        return lr

