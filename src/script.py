from helperMethods import *

def main():
        submission_list = getSubmissions()
        
        trending_list = analyzeSubmissions(submission_list)

        if(trending_list == None or len(trending_list) == 0):
            updateDataFiles(submission_list)
            closeFiles()
        else:
            for user in USER_NAME_LIST:
                sendNotification(trending_list, user)

            updateDataFiles(submission_list)
            closeFiles()
            
if __name__ == "__main__":
    main()