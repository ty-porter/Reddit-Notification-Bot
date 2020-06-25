# NOTE: This file is for reference only!

import praw
import time

#List of subreddits to keep track of
SUBREDDITS = [subreddit1, subreddit2, ..., subredditn]

#List of keywords for each subreddit
KEYWORDS = [[keywords11, keywords12, ..., keywords1n],
            [keywords21, keywords22, ..., keywords2n],
            [keywords31, keywords32, ..., keywords3n]]
#Keyword[i,:] is the keywords for SUBREDDIT[i]
#Some lines might have different number of elements (meaning some subreddits have different total of keywords)
#so smaller lines will have '' as elements past their length. (Empty linesa have all their elements as '')
#It must have the ability to have symbols as elements eg. @, #, $ etc


#List of "forbidden" keywords
FORBIDDEN_KEYWORDS = [[Fkeywords11, Fkeywords12, ..., Fkeywords1n],
            [Fkeywords21, Fkeywords22, ..., Fkeywords2n],
            [Fkeywords31, Fkeywords32, ..., Fkeywords3n]]
#Same rules apply as with keywords

#List of redditors to send the message to for each subreddit
REDDITORS = [Redditor1, Redditor2, ..., Redditorn]
#Some elements might be the same eg. [konsteva, konsteva, user12, Example2, user12, Example_124w45]




#Function to establish connection to reddit

def connect_to_reddit():
    reddit = praw.Reddit(
    username = '*****', #The username of the bot
    password = '*****', #The password of the bot account
    client_id = '*****', #Bot client ID
    client_secret = '*****', #Bots client secret
    user_agent = 'Describing the description quequequeque') #Bot Description.
    return reddit







#Function that sends the message
#The function should send the redditor the subreddit of the post, the title, selft text and link like that:
#Name_of_Subreddit: Submission_Title
#Submission_Selftext
#Link: Submission_link

def send_message(submission,USERNAME):
    #Checks if the title exceeds the 100 chars limit and if so it cut to 100 chars
    if len(submission.title) <= 100:
        title = submission.title
    else:
        title = submission.title[:97] + "..."
    try:
        reddit.redditor(USERNAME).message(submission_subreddit+": ", title, submission_selftext, "Link: "+submission.shortlink)
        #Some screen printing to make sure everything works
        print('Sent new message')
        print('New post in {}, Title: {}, Description: {}'.format(submission.subreddit, submission.title, submission.selftext))
    except Exception as e:
        print(e)
        time.sleep(60)







#Function to find submissions according to the list of keywords(if any) and the list of forbidden keywords

def find_submissions():
    try:
        while True:  #This might not be not needed (?)
            i = 0
            for subreddit in SUBREDDITS: #Going through all subs
                contains_Fkeyword = 'False'
                USERNAME = REDDITORS[i]
                for submission in reddit.subreddit(subreddit).stream.submissions(): #Streams new submissions
                    for Fkeyword in FORBIDDEN_KEYWORDS[i] :
                        if len(FORBIDDEN_KEYWORDS[i]) == 0:
                            break
                        elif Fkeyword.lower() in submission.title.lower() or Fkeyword.lower() in submission.selftext.lower():
                            contains_Fkeyword = 'True'
                            break; #If it finds a forbidden keyword it stops looking for others
                    if contains_Fkeyword == 'False':
                        for keyword in KEYWORDS[i]:
                            if len(FORBIDDEN_KEYWORDS[i]) == 0: #If it doesn't have keywords to search for it sends every new post
                                send_message(submission,USERNAME)
                                break                     
                            elif (keyword.lower() in submission.title or keyword.lower() in submission.selftext) and submission.created_utc > start_time: #if it contains the keyword either in title or selftext and the post was made after the script begin to run
                                send_message(submission,USERNAME)
                                break
                            elif contains_Fkeyword == 'True':
                                break; #If the submission contains a forbidden keyword there is no need to check if it has wanted keywords
                i = i+1
    except Exception as e:
        print(e)
        time.sleep(60)



if __name__ == '__main__':
    start_time = time.time()
    reddit = connect_to_reddit()
    find_submissions()