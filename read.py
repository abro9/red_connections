#!./venv/bin/python3

import praw

reddit = praw.Reddit('bot1')

subreddit = reddit.subreddit("learnpython")

for submission in subreddit.hot(limit=5):
    print("Title: ", submission.title)
    print("Test: ", submission.selftext)
    print("Score: ", submission.score)
    print("-------------------------------\n")

