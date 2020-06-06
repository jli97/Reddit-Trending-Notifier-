from helperMethods import *

def main():
        submission_list = getSubmissions()
        
        trending_list = analyzeSubmissions(submission_list)

        if(trending_list == None or len(trending_list) == 0):
            pullSubmissionData()
            closeFiles()
        else:
            sendNotification(trending_list, USER_NAME)
            pullSubmissionData()
            closeFiles()

if __name__ == "__main__":
    main()