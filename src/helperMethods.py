from pathlib import Path
import time
import praw
import csv
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from scipy.stats import norm
from configparser import ConfigParser

try:
    config = ConfigParser()
    config.read('user_info.cfg')
    reddit = praw.Reddit(client_id = config.get('main','client_id'),client_secret = config.get('main','client_secret'), username = config.get('main','username'), password = config.get('main','password'), user_agent='placeholder')
except:
    print("Error Occured in Reddit Authentication and/or Config file")

subreddit = reddit.subreddit("FrugalMaleFashionCDN")

''' ----------PARAMETERS----------- '''
USER_NAME = config.get('main', 'username') # Account the message is sent to, can be replaced with another username

num_hours = 12      # Max age a post can be to be included in data
bucket_1 = [0,4]    # You can edit the hour buckets
bucket_2 = [4,8]    # [0,4] = 0 < submission_age <= 4 hours
bucket_3 = [8,12]

sample_size = 100   # Minimum sample size required for regression

alpha = 0.95        # For the regression prediction interval
                    # Change it between 0-1
                    # Higher value = less notifications, lower value = more notifications
''' ------------------------------- '''
unix_hour = 60*60 

path = Path(__file__).absolute()                    # Needs to be written with two lines for windows task scheduler to work 
data_folder = path.parent.parent / "datafiles"      # Bug with task scheduler's usage of absolute paths

file_1 = open(data_folder / "bucket_1.csv", 'a+', newline='')
file_2 = open(data_folder / "bucket_2.csv", 'a+', newline='')
file_3 = open(data_folder / "bucket_3.csv", 'a+', newline='')

'''GET METHODS'''
def getSubmissions():
    #Return submission_list
    submission_list = []

    for submission in subreddit.new(): 
        age = time.time() - submission.created_utc 
        if(age > (num_hours*60*60)): 
            break
        if(age < (num_hours*60*60) and not submission.stickied): # Post is less than num_hours hrs old
            submission_list.append(submission)
    return submission_list 
    
def getAge(submission):
    return time.time() - submission.created_utc

def getBucketFile(submission_age):
    if(bucket_1[0]*unix_hour <= submission_age <= bucket_1[1]*unix_hour):
        file = file_1
    elif(bucket_2[0]*unix_hour < submission_age <= bucket_2[1]*unix_hour):
        file = file_2
    else:
        file = file_3
    return file

''' ANALYSIS METHODS '''
def analyzeSubmissions(submission_list):
    #Analysis of submissions in submission_list and returns list of trending submissions
    trending_list = []
    try:
        for submission in submission_list:
            age = getAge(submission)
            file = getBucketFile(age)
            df = pd.read_csv(file.name)

            lr = regression(df)
            if(lr == None):
                continue
            lr_input = np.array([age]).reshape(-1,1)
            prediction = lr.predict(lr_input)

            y_actual = df['upvotes'].values.reshape(-1,1)
            x = df['age'].values.reshape(-1,1)
            y_model = lr.predict(x)

            upper_prediction = getUpperPrediction(prediction, y_actual, y_model, alpha)

            if(submission.score > upper_prediction):
                trending_list.append(submission)
        
        return trending_list
    except:
        print("An Exception Occured in analyzeSubmissions")

def regression(df):
    if(len(list(df)) < sample_size): #If there aren't enough entries based on sample_size dont analyze and return null
        return None

    y = df['upvotes'].values.reshape(-1,1)
    x = df['age'].values.reshape(-1,1)
    try:
        lr_obj = LinearRegression(fit_intercept=False).fit(x,y)
    except Exception as e:
        print(e)
    return lr_obj

def getUpperPrediction(prediction, y_actual, y_model, alpha):
    #stdev of y_actual
    sum_errs = np.sum((y_actual - y_model)**2)
    stdev = np.sqrt(1 / (len(y_actual) - 2) * sum_errs)

    #Interval
    prob_value = 1 - ((1 - alpha) / 2)
    z_score = norm.ppf(prob_value)
    interval = z_score * stdev

    #generate prediction interval lower and upper bound
    ret = prediction + interval
    return ret

''' I/O METHODS ''' 
def pullSubmissionData(): #Records id and upvotes for posts less than 2 days old in a csv
    header = ["id", "upvotes", "age"]

    for submission in subreddit.new():
        age = time.time() - submission.created_utc
        if((age > (num_hours*60*60))): #If post is older than 12 hours
            break
        if(submission.stickied):
            continue
        
        if(submission.upvote_ratio < 0.5 and age > 60*60): # % of upvotes, ignore negative posts that are more than 1 hour old
            continue

        entry = [submission.id, submission.score, age]    
        print(submission.id)
        print(entry)
        file = getBucketFile(age)

        file.seek(0,0)
        reader = csv.reader(file)
        writer = csv.writer(file)
        if(len(list(reader)) == 0):
            writer.writerow(header)
            writer.writerow(entry)
        else:
            writer.writerow(entry)
            print("Added to "+ file.name)

def closeFiles():
    file_1.close
    file_2.close
    file_3.close

''' REDDIT MESSAGING ''' 
def sendNotification(trending_list, username):
    if(len(trending_list) == 0):
        return
    
    msg ="The following posts(s) are trending:\n"

    for submission in trending_list:
        msg = msg + "["+submission.title+"]"+"("+submission.url+")\n"

    try:
        reddit.redditor(username).message("Trending Notification", msg)
    except Exception as e:
        print(e)
        
