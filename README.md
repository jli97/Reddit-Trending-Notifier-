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
4. Go to "Actions", and create a new Action
   - Program/script is the absolute path to python.exe
   - Add arguments is just script.py
   - Start in (optional) is the path to the src folder (C:...\Reddit-Trending-Notifier\src)
![alt text](https://github.com/jli97/Reddit-Trending-Notifier-/blob/master/extras/readme_task.png)
5. Go to "Triggers", Click "Repeate task every ..." and have it run every 1 hour and for a duration of indefinitely

Once that is done, the script is ready to go. 

## How it Works
The script runs with the help of a script automation software/service. Everytime it runs, it pulls new submissions from the provided subreddit and analyzes each submission to determine whether or not it is "trending". To determine whether the post is trending, the script takes the existing data and runs a linear regression. It then uses the model to determine whether the new submission is significant enough to warrant a notifiacation. At the end, the new submissions will be added to the dataset. Datasets are split into 3 buckets based on age ranges which allows for more accurate models (upvotes tend to accelerate in the first couple hours and then trail off). Datasets also have a max sample size and will automatically delete the oldest entries to make space for new entries. 

## Customization 
The sciprt is highly customizable. Within helperMethods.py there is a PARAMETERS section to customize the script to fit your needs.

If you want to use the script for another subreddit, you will need to delete the existing csv files in the datafiles folder and change the subreddit variable in helperMethods.py. 
