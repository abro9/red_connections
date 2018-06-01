#!./venv/bin/python3

import praw
import prawcore
import json

data_input_path = './data/usernames_POPULAR_10000.txt'
data_output_path = './usernames_POPULAR_10000.json'

reddit = praw.Reddit('bot1')

redditor_dict = {}

def get_submission_subreddit_dict(username):
    subreddit_dict = {}

    try:
        for submission in reddit.redditor(username).submissions.new(limit=None):
            sub_name = submission.subreddit.display_name
            if sub_name in subreddit_dict.keys():
                subreddit_dict[sub_name] += 1
            else:
                subreddit_dict[sub_name] = 1
    except (KeyboardInterrupt, SystemExit):
        raise
    except:
        pass

    return subreddit_dict

def get_comment_subreddit_dict(username):
    subreddit_dict = {}

    try:
        for comment in reddit.redditor(username).comments.new(limit=None):
            sub_name = comment.subreddit.display_name
            if sub_name in subreddit_dict.keys():
                subreddit_dict[sub_name] += 1
            else:
                subreddit_dict[sub_name] = 1
    except (KeyboardInterrupt, SystemExit):
        raise
    except:
        pass

    return subreddit_dict

def build_user_dict(username):
    user_dict = {}
    user_dict['submissions'] = get_submission_subreddit_dict(username)
    user_dict['comments'] = get_comment_subreddit_dict(username)

    return user_dict

def build_user_list(input_file):
    user_list = []

    with open(input_file, 'r') as f:
        for line in f:
            user_list.append(line.strip())

    return user_list

if __name__ == "__main__":

# user = 'raymincer'

# redditor_dict[user] = build_user_dict(user)
# print('Submissions: ' + str(redditor_dict[user]['submissions']))
# print('Comments: ' + str(redditor_dict[user]['comments']))

    redditor_dict = {}
    user_list = build_user_list(data_input_path)

    for user in user_list:
        redditor_dict[user] = build_user_dict(user)

        dict_len = len(redditor_dict)
        user_list_len = len(user_list)

        if dict_len % 50 == 0:
            print('{0} of {1} done'.format(dict_len,  user_list_len))

    with open(data_output_path, 'w') as f:
        json.dump(redditor_dict, f)

