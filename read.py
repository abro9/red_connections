#!./venv/bin/python3

import praw
import prawcore
import json
from os import listdir

#data_input_path = '/home/pi/projects/red_connections/data/usernames/usernames_ALL_5000_0.txt'
#data_output_path = '/home/pi/projects/red_connections/data/json/usernames_ALL_5000_0.json'

input folder = '/home/pi/projects/red_connections/data/usernames/'
output folder = '/home/pi/projects/red_connections/data/json/'

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

# Returnes target filename (no extension)
def get_target_file(input_filelist, output_filelist):

    input_dict_all = {}
    output_dict_all = {}

    for (i, f) in list(enumerate(input_filelist)):

        split_list = f.replace('.', '_').split('_')

        fdict = {}
        fdict['name'] = f[:-4]
        fdict['index'] = i
        fdict['version'] = split_list[3]
        fdict['month'] = split_list[4]
        fdict['day'] = split_list[5]
        fdict['year'] = split_list[6]

        input_dict_all[f] = fdict

    current_target = ''
    current_target_date = [13, 32, 3000]

    for f, fdict in input_dict_all:
        if fdict[:


# Returns dictionary of parsed filenames
def parse_io_filenames(input_folder, output_folder):

    input_filelist = listdir(input_folder)
    output_filelist = listdir(input_folder)
    target_filename_base = get_target_file(input_filelist, output_filelist)
    
    data_input_path = input_folder + target_filename_base + '.txt'
    data_output_path = output_folder + target_filename_base + '.json'

    return (data_input_path, data_output_path)

if __name__ == "__main__":

    data_input_path, data_output_path = parse_io_filenames(input_folder, output_folder)

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

