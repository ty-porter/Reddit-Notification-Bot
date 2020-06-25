import json
import os
import praw

# Try to import our config class, otherwise just stub it so it doesn't accidentally break
try:
    from env import Config
except ImportError:
    from stub_env import Config

class Bot:

    __CONFIG_PATH = 'config.json'

    def __init__(self):
        self.reddit = self.load_reddit()
        self.config = self.load_notification_configuration(self.__CONFIG_PATH)

    def load_reddit(self):
        # Check where the script is running. If it's on a local machine, set the vars needed.
        # Otherwise, continue on, assuming these vars are set on Heroku.
        if 'SCRIPT_ENV' not in os.environ or os.environ['SCRIPT_ENV'] in ['test', 'development']:
            Config.set_env_vars()

        reddit = praw.Reddit(client_id=os.environ['REDDIT_CLIENT_ID'],
                            client_secret=os.environ['REDDIT_CLIENT_SECRET'],
                            user_agent=os.environ['REDDIT_USER_AGENT'],
                            username=os.environ['REDDIT_USERNAME'],
                            password=os.environ['REDDIT_PASSWORD'])

        return reddit

    def find_submissions(self):
        # Use a multireddit to stream from multiple subreddits instead of instantiating a new stream for each subreddit,
        # the other way would iterate over EVERY submission in EVERY subreddit in the master subreddit list for all new submissions
        multireddit = '+'.join( self.config.keys() )

        # Stream the multireddit, set skip_existing to True to skip any posts that are already in the sub
        for submission in self.reddit.subreddit(multireddit).stream.submissions(skip_existing=True):
            # Since we use a multireddit, we need to know which subreddit configuration to load...
            # This finds the subreddit, and loads the correct config.
            subreddit = submission.subreddit.display_name
            subreddit_data = self.config[subreddit]

            # Pull a list of keywords out of the config file
            blacklisted_keywords = subreddit_data['blacklisted_keywords']
            keywords = subreddit_data['keywords']

            # Call lower() on submission title and selftext once rather than for every keyword check
            submission_title = submission.title.lower()
            # If submission isn't a self post, we can ignore it by setting to empty string
            submission_selftext = submission.selftext.lower() if submission.is_self else ''
            # Concat these two to make searching easier
            target_text = ' '.join([submission_title, submission_selftext])

            # Intentionally check blacklist first, we will always search for all blacklisted keywords,
            # but won't need to search for all keywords (potentially)
            if not self.has_keyword(target_text, blacklisted_keywords) and self.has_keyword(target_text, keywords):
                # Message the redditors from the config if this check passes
                redditors = subreddit_data['redditors']
                    
                for redditor in redditors:
                    if not submission.author.name == redditor:
                        self.send_message(submission, redditor)
                    else:
                        print('Skipping message, submission author {} is the same as the target user.'.format(redditor))

    def has_keyword(self, target_text, keywords):
        # Check if a keyword is in the target
        for keyword in keywords:
            if keyword.lower() in target_text:
                return True

        return False

    def send_message(self, submission, username):
        # Build up a good title
        title = "{}: {}".format(submission.subreddit.display_name, submission.title)

        # Check if it's too big, and trunc it if so
        if len(title) > 100: 
            title = title [:97] + '...'

        # Build the message body, since Redditor.message() takes two arguments
        # The double newlines ( \n\n ) make the link appear with a space at the end of the post
        # Also account for empty selftext if it's a link post...
        newlines = "\n\n" if submission.is_self else ''
        message_body = submission.selftext + newlines + 'Link: ' + submission.shortlink

        try:
            self.reddit.redditor(username).message(title, message_body)
            # Some screen printing to make sure everything works
            print('Sent new message')
            print('New post in {}, Title: {}, Description: {}'.format(submission.subreddit.display_name, submission.title, submission.selftext))
        except Exception as e:
            print(e)
            time.sleep(60)


    def load_notification_configuration(self, path):
        # Reads a JSON file to pull out notification configuration.
        # We can treat this as a dict, rather than multiple nested arrays that need to be tracked.
        with open(path) as f:
            data = json.load(f)

        return data

if __name__ == '__main__':
    Bot().find_submissions()