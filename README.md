# Reddit Notification Bot

This bot is a configurable bot to notify redditors when a keyword is posted in a desired subreddit. It supports keywords, blacklisted keywords, and messaging multiple users per subreddit.

RNB is designed to be hosted both locally and on Heroku.

# Local Installation

Local installation of RNB requires 2 config files, `config.json` and `env.py`. If this is your first time using RNB, you'll notice that the `config.json` file already exists, but `env.py` does not -- This is because sensitive credentials live in this file that should not be committed to source control.

There is an install script to copy a template to the correct location:

```
sh install.sh
```

This will install the correct `env.py` and you can configure it with the correct credentials.

### `config.json`

For this file, you'll need to add subreddits. A basic configuration might look like this:

```json
{
  "test": {
    "keywords": [
      "test"
    ],
    "blacklisted_keywords": [
      "bot"
    ],
    "redditors": [
      "pawptart"
    ]
  }
}
```

This configuration will send a message to `/u/pawptart` every time a submission to `/r/test` includes `test` but not `bot`. You can add an arbitrary number of subreddits, keywords, blacklists, and redditors:

```json
{
  "test": {
    "keywords": [
      "keyword1",
      "keyword2",
      "keyword3",
      "keyword4",
      "keyword5"
    ],
    "blacklisted_keywords": [
      "blacklisted_keyword1",
      "blacklisted_keyword2",
      "blacklisted_keyword3",
      "blacklisted_keyword4",
      "blacklisted_keyword5"
    ],
    "redditors": [
      "test_redditor_1",
      "test_redditor_2"
    ]
  },
  "requestabot": {
    "keywords": [
      "keyword1",
      "keyword2",
      "keyword3",
      "keyword4",
      "keyword5"
    ],
    "blacklisted_keywords": [
      "blacklisted_keyword1",
      "blacklisted_keyword2",
      "blacklisted_keyword3",
      "blacklisted_keyword4",
      "blacklisted_keyword5"
    ],
    "redditors": [
      "test_redditor_1",
      "test_redditor_2"
    ]
  }
}
```

These configurations would message 2 separate users for every keyword trigger.

# Heroku Deployment

Coming soon!