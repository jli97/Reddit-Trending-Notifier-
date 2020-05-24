import getData
import time
from sklearn.metrics import mean_squared_error
from scipy.stats import norm
import numpy as np

def main():
    sub_name = "FrugalMaleFashionCDN" #Provide subreddit name
    sub_data = getData.Data(sub_name)

    print(sub_data.lr_obj.coef_)
    for submission in sub_data.new_posts: # Only checks posts created within 24hours
        print(submission.title)
        if(isTrending(sub_data, submission)):
            msg = "This [post]("+submission.permalink+ ") is trending on /r/ " + sub_name
            #sub_data.reddit.redditor('jonyface').message("Trend Notification",msg) #Provide username to send messages to
        

def isTrending(sub_data, submission): 
    """
    Uses basic linear regression to determine if post is trending 
    Accuracy of the model can be adjusted by changing the input alpha (0-1) in getUpperPrediction. Higher alpha = more accurate/less posts
    """
    x = sub_data.data_frame.iloc[:,0].copy()
    x = x.values.reshape(-1,1) 
    y_actual = sub_data.data_frame.iloc[:,1].copy()
    y_actual = y_actual.values.reshape(-1,1)

    pred = sub_data.lr_obj.coef_ * (time.time() - submission.created_utc)
    y_model = sub_data.lr_obj.predict(x)
    
    upper_pred = getUpperPrediction(pred,y_actual,y_model,0.80)
    
    print(" age is "+ str(time.time()-submission.created_utc))
    print(" upper_pred is "+ str(upper_pred))
    print(" pred is "+ str(pred))
    print(" actual is " + str(submission.score))
    
    if (submission.score > upper_pred):
        return True
    else:
        return False


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

if __name__ == "__main__":
    main()