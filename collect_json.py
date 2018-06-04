#!./venv/bin/python3

import json
from os import listdir

user_set = set()
user_dict = {}
duplicates = []
duplicates_dict = {}

input_path = '/home/pi/projects/red_connections/data/json/'
output_path = '/home/pi/projects/red_connections/data/all_json.json'

dir_list = listdir(input_path)

for user_file in dir_list:
    current_input_file = '/home/pi/projects/red_connections/data/json/{}'.format(user_file)
    with open(current_input_file, 'r') as f:
        for line in f:
            current_import_dict = json.loads(line)
            for k, v in current_import_dict.items():
                if k in user_set:
                    user_dict[k + '__DUP__'] = v
                    duplicates_dict[k]['seen_count'] += 1
                    duplicates_dict[k]['in_files'].append(user_file[:-5])
                    #duplicates.append('{} -- {}'.format(k, user_file))
                else:
                    user_set.add(k)
                    duplicates_dict[k] = {'seen_count': 1, 'in_files': [user_file[:-5]]}
                    user_dict[k] = v

with open(output_path, 'w') as f:
    json.dump(user_dict, f)

for k in duplicates_dict.keys():
    if duplicates_dict[k]['seen_count'] > 1:
        duplicates.append('{} -- {} -- {}'.format(k,
                                                  duplicates_dict[k]['seen_count'],
                                                  duplicates_dict[k]['in_files']))

with open(input_path[:-5] + 'duplicates.txt', 'w') as f:
    for line in duplicates:
        f.write('{}\n'.format(line))

