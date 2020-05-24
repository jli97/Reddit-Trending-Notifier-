import praw

reddit = praw.Reddit(client_id = 'aM_mGMSXor7avg',client_secret = 'rlfl7DoUGE74y_5UlcP2jLntoVw', username='PRAW_97', password='123456789j', user_agent='Better Trending')

print(reddit.subreddit("pics"))