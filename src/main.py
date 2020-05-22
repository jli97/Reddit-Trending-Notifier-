import getData
import time
from sklearn.metrics import mean_squared_error
from scipy.stats import norm
import numpy as np
#gkm73p


def main():
    sub_name = "FrugalMaleFashionCDN"
    sub_data = getData.Data(sub_name)


    for submission in sub_data.new_posts: # Only checks posts created within 24hours
        print(submission.title)
        if(isTrending(sub_data, submission)):
            msg = "This [post]("+submission.permalink+ ") is trending on /r/ " + sub_name
            #sub_data.reddit.redditor('jonyface').message("Trend Notification",msg)
        

def isTrending(sub_data, submission):
    x = sub_data.data_frame.iloc[:,0].copy()
    x = x.values.reshape(-1,1) 
    y_actual = sub_data.data_frame.iloc[:,1].copy()
    y_actual = y_actual.values.reshape(-1,1)

    pred = sub_data.lr_obj.coef_ * (time.time() - submission.created_utc)
    y_model = sub_data.lr_obj.predict(x)
    
    upper_pred = getUpperPrediction(pred,y_actual,y_model,0.95)
    
    if (submission.score > upper_pred):
        return True
    else:
        return False


def getUpperPrediction(prediction, y_actual, y_model, pi):
    #stdev of y_actual
    sum_errs = np.sum((y_actual - y_model)**2)
    stdev = np.sqrt(1 / (len(y_actual) - 2) * sum_errs)

    #Interval
    prob_value = 1 - ((1 - pi) / 2)
    z_score = norm.ppf(prob_value)
    interval = z_score * stdev

    #generate prediction interval lower and upper bound
    ret = prediction + interval
    return ret

if __name__ == "__main__":
    main()