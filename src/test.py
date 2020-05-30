import praw
from sklearn.linear_model import LinearRegression
import pandas as pd
import numpy as np
from scipy.stats import norm
import csv 
from configparser import ConfigParser

config = ConfigParser()
config.read('user_info_local.cfg')

reddit = praw.Reddit(client_id = config.get('main','client_id'),client_secret = config.get('main','client_secret'), username = config.get('main','username'), password = config.get('main','password'), user_agent='placeholder')
subreddit = reddit.subreddit("FrugalMaleFashionCDN")

file_1 = open("bucket_1_local.csv",'a+', newline='')

def regression(df):
    if(len(list(df)) < 1): #If there aren't 100 entries, dont analyze and return null
        return None

    y = df['upvotes'].values.reshape(-1,1)
    x = df['age'].values.reshape(-1,1)

    ret = LinearRegression(fit_intercept=False).fit(x,y)

    return ret

for submission in subreddit.new(): 
    print(submission.title)

file_1.seek(0,0)
reader = csv.reader(file_1)
print(len(list(reader)))
print("got here")