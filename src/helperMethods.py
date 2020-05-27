import time
import praw
import csv
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from scipy.stats import norm

''' ----------PARAMETERS----------- '''
reddit = praw.Reddit(client_id = 'aM_mGMSXor7avg',client_secret = 'rlfl7DoUGE74y_5UlcP2jLntoVw', username='PRAW_97', password='123456789j', user_agent='Better Trending')
subreddit = reddit.subreddit("FrugalMaleFashionCDN")

num_hours = 12
bucket_1 = [0,4]
bucket_2 = [4,8]
bucket_3 = [8,12]

alpha = 0.95 # For the regression prediction interval
             # Change it between 0-1
             # Higher value = less notifications, lower value = more notifications
''' ------------------------------- '''
unix_hour = 60*60

file_1 = open("bucket_1.csv", 'a+', newline='')
file_2 = open("bucket_2.csv", 'a+', newline='')
file_3 = open("bucket_3.csv", 'a+', newline='')
file_dict = {1:file_1, 2:file_2, 3:file_3}

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

def regression(df):
    if(len(list(df)) < 100): #If there aren't 100 entries, dont analyze and return null
        return None

    y = df['upvotes'].values.reshape(-1,1)
    x = df['age'].values.reshape(-1,1)

    ret = LinearRegression(fit_intercept=False).fit(x,y)

    return ret

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

''' I/O Methods ''' 
def pullSubmissionData(): #Records id and upvotes for posts less than 2 days old in a csv
    header = ["id", "upvotes", "age"]

    for submission in subreddit.new():
        age = time.time() - submission.created_utc
        if((age > (num_hours*60*60))): #If post is older than 12 hours
            break
        if(submission.stickied):
            continue

        entry = [submission.id, submission.score, age]    

        file = getBucketFile(age)

        reader = csv.reader(file)
        writer = csv.writer(file)
        if(len(list(reader)==0)):
            writer.writerow(header)
            writer.writerow(entry)
        else:
            writer.writerow(entry)

def closeFiles():
    file_1.close
    file_2.close
    file_3.close

''' Reddit Messaging ''' 
def sendNotification(trending_list, username):
    #compose a single mesesage with all links
    msg =""
    reddit.redditor(username).message("Trend Notification",msg) #Provide username to send messages to
    
