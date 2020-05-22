import getData
import datetime

def main():
    name = "FrugalMaleFashionCDN"
    sub_data = getData.Data(name)

    for submission in sub_data.new_posts: # Submissions that are less than 24hrs old
        if(isTrending(sub_data, submission)):
            #Send message

def isTrending(sub_data, submission):
    

