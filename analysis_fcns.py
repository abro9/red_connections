#!./venv/bin/python3

import json
import datetime
from os import listdir

input_file = './data/json/usernames_POPULAR_1000.json'
output_path = '/home/pi/projects/red_connections/data/quick_stats/'
NUM_TO_OUTPUT = 10

with open(input_file, 'r') as f:
    for line in f:
        import_dict = json.loads(line)

def user_pairs(user_dict):
    user_c_dict = user_dict['comments']
    user_s_dict = user_dict['submissions']

    comment_pair_dict = {}
    user_comment_subreddits = sorted(list(user_c_dict.keys()))
    num_comment_subs = len(user_comment_subreddits)

    comment_actions = 0

    for value in user_c_dict.values():
        comment_actions += value

    if num_comment_subs < 2:
        return {}

    for start, sub1 in enumerate(user_comment_subreddits):
        for sub2 in range(start, num_comment_subs):
            sub2 = user_comment_subreddits[sub2]
            try:
                if sub1 != sub2:
                    new_key = '{}-{}'.format(sub1, sub2)
                    comment_pair_dict[new_key] = (user_c_dict[sub1] + user_c_dict[sub2]) * 100 / comment_actions
            except KeyError:
                print('keyerror: {} - {}'.format(sub1, sub2))

    return comment_pair_dict

pairs_dict = user_pairs(import_dict['intothequicksand'])

for k, v in pairs_dict.items():
    print('{} -- {}'.format(k, v))

print(max(pairs_dict.values()))
print(min(pairs_dict.values()))
