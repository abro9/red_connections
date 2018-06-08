#!./venv/bin/python3

import json
import datetime
from os import listdir

input_file = './data/all_json.json'
output_path = './data/subreddit_list.txt'

with open(input_file, 'r') as f:
    for line in f:
        import_dict = json.loads(line)

subreddit_set = set()

for user in import_dict.keys():
    for sub in import_dict[user]['submissions'].keys():
        subreddit_set.add(sub)
    for sub in import_dict[user]['comments'].keys():
        subreddit_set.add(sub)

with open(output_path, 'w+') as f:
    for sub in subreddit_set:
        f.write('{}\n'.format(sub))

