#!./venv/bin/python3

import praw
import json

reddit = praw.Reddit('bot1')

input_file = './data/subreddit_list.txt'
output_path = './data/sub_counts.json'

sub_list = []
sub_count_dict = {}

with open(input_file, 'r') as f:
    for line in f:
        sub_list.append(line.strip())

num_subs = len(sub_list)

for sub in sub_list:
    try:
        sub_count = reddit.subreddit(sub).subscribers
    except (KeyboardInterrupt, SystemExit):
        raise
    except:
        sub_count = -1

    sub_count_dict[sub] = sub_count
    num_done = len(sub_count_dict)

    if num_done % 50 == 0:
        print('{} of {} done'.format(num_done, num_subs))

with open(output_path, 'w+') as f:
    json.dump(sub_count_dict, f, sort_keys=True, indent=4)

