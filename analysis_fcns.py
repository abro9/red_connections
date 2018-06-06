#!./venv/bin/python3

import json
import datetime
from os import listdir

input_file = './data/json/usernames_POPULAR_10000.json'
output_path = './data/big_files/popular_10000_pairs.json'
NUM_TO_OUTPUT = 10

with open(input_file, 'r') as f:
    for line in f:
        import_dict = json.loads(line)

def calc_pairs(sub_dict):
    pair_dict = {}
    sub_list = sorted(list(sub_dict.keys()))
    num_subs = len(sub_list)

    num_actions = 0

    for value in sub_dict.values():
        num_actions += value

    if num_subs < 2:
        return {}

    for start, sub1 in enumerate(sub_list):
        for sub2 in range(start, num_subs):
            sub2 = sub_list[sub2]
            try:
                if sub1 != sub2:
                    new_key = '{}-{}'.format(sub1, sub2)
                    pair_dict[new_key] = (sub_dict[sub1] + sub_dict[sub2]) * 100 / num_actions
            except KeyError:
                print('keyerror: {} - {}'.format(sub1, sub2))
    return pair_dict

def user_pairs(user_dict):
    c_pair_dict = calc_pairs(user_dict['comments'])
    s_pair_dict = calc_pairs(user_dict['submissions'])

    total_pair_dict = { k: c_pair_dict.get(k, 0) + s_pair_dict.get(k, 0) for k in set(c_pair_dict) | set(s_pair_dict) }

    output_dict = {'total': total_pair_dict, 'comments': c_pair_dict, 'submissions': s_pair_dict}

    return output_dict

def calc_all_user_pairs(j_dict):
    user_pairs_dict = {}
    for user in j_dict.keys():
        user_pairs_dict[user] = user_pairs(j_dict[user])
    return user_pairs_dict

pairs_dict = calc_all_user_pairs(import_dict)
#print(pairs_dict)
with open(output_path, 'w+') as f:
    json.dump(pairs_dict, f)

