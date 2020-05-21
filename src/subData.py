import praw
import math

reddit = praw.Reddit(client_id = 'aM_mGMSXor7avg',client_secret = '	rlfl7DoUGE74y_5UlcP2jLntoVw', username='PRAW_97', password='123456789j', user_agent='Better Trending')
sub_name = "FrugalMaleFashionCDN" #Make this an input later
subreddit = redd.subreddit(sub_name)

def getAverageUpVotes(sub_name):
    sum = 0
    count = 0 #If subreddit has less than 50 submissions
    for submission in subreddit.hot(limit=50):
        sum = sum + submission.score
        count = count + 1

    return sum/count

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