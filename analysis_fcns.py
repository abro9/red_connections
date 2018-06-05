#!./venv/bin/python3

import json
import datetime
from os import listdir

input_file = './data/json/usernames_POPULAR_1000.json'
#output_path = '/home/pi/projects/red_connections/data/quick_stats/'
NUM_TO_OUTPUT = 10

with open(input_file, 'r') as f:
    for line in f:
        import_dict = json.loads(line)

def user_pairs(user_dict):
    pair_dict = {}
    user_subreddits = sorted(list(user_dict.keys()))
    list_len = len(user_subreddits)

    #print(user_subreddits)
    #print(user_dict)
    total_actions = 0

    for value in user_dict.values():
        total_actions += value

    if list_len < 2:
        return {}

    for start, sub1 in enumerate(user_subreddits):
        for sub2 in range(start, list_len):
            sub2 = user_subreddits[sub2]
            #subs = sorted(sub1, sub2)
            try:
                if sub1 != sub2:
                    new_key = '{}-{}'.format(sub1, sub2)
                    pair_dict[new_key] = (user_dict[sub1] + user_dict[sub2]) * 100 / total_actions
            except KeyError:
                print('keyerror: {} - {}'.format(sub1, sub2))

    return pair_dict

#print(import_dict['intothequicksand']['comments'])
pairs_dict = user_pairs(import_dict['intothequicksand']['comments'])
#print(pairs_dict)

for k, v in pairs_dict.items():
    print('{} -- {}'.format(k, v))

print(max(pairs_dict.values()))
print(min(pairs_dict.values()))
