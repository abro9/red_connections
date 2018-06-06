#!./venv/bin/python3

import json
import datetime
from os import listdir

input_file = './data/big_files/all_2000_0_pairs.json'
output_path = './data/big_files/all_2000_0_pairs_comb.json'
#input_file = './data/json/usernames_ALL_2000_0.json'
#output_path = './data/big_files/all_2000_0_pairs.json'

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

def sort_dict_by_value(some_dict):
    sorted_list = [(k, some_dict[k]) for k in sorted(some_dict, key=some_dict.get, reverse=True)]
    return sorted_list

def combine(pair_dict, section):
    comb_dict = {}
    for user in pair_dict.keys():
        for sub_pair, count in pair_dict[user][section].items():
            if sub_pair in comb_dict.keys():
                comb_dict[sub_pair] += count
            else:
                comb_dict[sub_pair] = count
    return comb_dict

def combine_user_pairs(pair_dict):
    comb_c_dict = combine(pair_dict, 'comments')
    comb_s_dict = combine(pair_dict, 'submissions')
    comb_t_dict = combine(pair_dict, 'total')

    full_pair_dict = {'total': comb_t_dict, 'comments': comb_c_dict, 'submissions': comb_s_dict}
    return full_pair_dict

if __name__ == "__main__":
    #pairs_dict = calc_all_user_pairs(import_dict)
    comb_dict = combine_user_pairs(import_dict)

    sorted_pair_list = sort_dict_by_value(comb_dict['total'])
    for k, v in sorted_pair_list[:50]:
        print('{} -- {}'.format(k, v))

    #with open(output_path, 'w+') as f:
    #    json.dump(comb_dict, f)

