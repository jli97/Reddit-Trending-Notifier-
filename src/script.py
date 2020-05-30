from helperMethods import *

''' Provide your Reddit Username '''
USER_NAME = ""
''' ---------------------------- '''
def main():
        submission_list = getSubmissions()
        
        trending_list = analyzeSubmissions(submission_list)

        if(trending_list == None or len(trending_list) == 0):
            closeFiles()
            pullSubmissionData()
        else:
            sendNotification(trending_list, USER_NAME)
            closeFiles()
            pullSubmissionData()

if __name__ == "__main__":
    main()