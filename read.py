#!./venv/bin/python3

import praw

reddit = praw.Reddit('bot1')

redditor_dict = {}

def get_submission_subreddit_dict(username):
    subreddit_dict = {}

    for submission in reddit.redditor(username).submissions.new(limit=None):
        sub_name = submission.subreddit.display_name
        if sub_name in subreddit_dict.keys():
            subreddit_dict[sub_name] += 1
        else:
            subreddit_dict[sub_name] = 1

    return subreddit_dict

def get_comment_subreddit_dict(username):
    subreddit_dict = {}

    for comment in reddit.redditor(username).comments.new(limit=None):
        #print(comment.subreddit)
        sub_name = comment.subreddit.display_name
        if sub_name in subreddit_dict.keys():
            subreddit_dict[sub_name] += 1
        else:
            subreddit_dict[sub_name] = 1

    return subreddit_dict

def build_user_dict(username):
    user_dict = {}
    user_dict['submissions'] = get_submission_subreddit_dict(username)
    user_dict['comments'] = get_comment_subreddit_dict(username)

    return user_dict

user = 'raymincer'

redditor_dict[user] = build_user_dict(user)
print('Submissions: ' + str(redditor_dict[user]['submissions']))
print('Comments: ' + str(redditor_dict[user]['comments']))

