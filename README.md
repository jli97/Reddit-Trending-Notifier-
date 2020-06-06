# Reddit Trending Notifier
This script was made to notify the user of any posts that recieved significantly higher upvotes relative to their age. The datafiles provided are for r/FrugalMaleFashionCDN, but the script can be applied to any other subreddit as well. 

## Usage
This script was made to run with Windows Task Scheduler, but any other scirpt automation service will work.

Setting up Reddit API
1. Go to your Preferences on Reddit 
2. Click on Apps and create a new app
3. Copy the required fields into user_info.cfg (Client_id is the text under the name of the app)

Setting up Task Scheduler
1. Open Task Scheduler
2. Create Task
3. Select Run whether user is logged in or not (this will prevent a console from popping up each time the script is run)
4. Go to "Actions"
![alt text](https://github.com/jli97/Reddit-Trending-Notifier-/blob/master/extras/readme_task.png)

Once that is done, the script is ready to go. Have it run every hour through 
