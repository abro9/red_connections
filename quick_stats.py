#!./venv/bin/python3

import json
import datetime
from os import listdir

user_dict = {}
sub_dict_s = {} #submissions
sub_dict_c = {} #comments
sub_dict_total = {}

input_file = '/home/pi/projects/red_connections/data/all_json.json'
output_path = '/home/pi/projects/red_connections/data/quick_stats/'
NUM_TO_OUTPUT = 10

with open(input_file, 'r') as f:
    for line in f:
        import_dict = json.loads(line)
    for username, v in import_dict.items():
        for sub, count in v['submissions'].items():
            if sub in sub_dict_s.keys():
                sub_dict_s[sub] += count
            else:
                sub_dict_s[sub] = count
        
        for sub, count in v['comments'].items():
            if sub in sub_dict_c.keys():
                sub_dict_c[sub] += count
            else:
                sub_dict_c[sub] = count

sub_dict_total = { k: sub_dict_s.get(k, 0) + sub_dict_c.get(k, 0) for k in set(sub_dict_s) | set(sub_dict_c) }

sorted_subs_s = [(k, sub_dict_s[k]) for k in sorted(sub_dict_s, key=sub_dict_s.get, reverse=True)]
sorted_subs_c = [(k, sub_dict_c[k]) for k in sorted(sub_dict_c, key=sub_dict_c.get, reverse=True)]
sorted_subs_total = [(k, sub_dict_total[k]) for k in sorted(sub_dict_total, key=sub_dict_total.get, reverse=True)]

dt = datetime.datetime.today()

file_list = listdir(output_path)
num = 0
out_filename = 'quick_stats_{}.{}.{}_{}.txt'.format(dt.month, dt.day, dt.year, num)

while out_filename in file_list:
    num += 1
    out_filename = 'quick_stats_{}.{}.{}_{}.txt'.format(dt.month, dt.day, dt.year, num)

total_output_path = '{}{}'.format(output_path, out_filename)

with open(total_output_path, 'w+') as f:
    f.write('Top {} subs by activity (total)\n'.format(NUM_TO_OUTPUT))
    for sub_tuple in sorted_subs_total[:NUM_TO_OUTPUT]:
        f.write('{} - {}\n'.format(sub_tuple[0], sub_tuple[1]))
    f.write('\n')

    f.write('Top {} subs by activity (submissions)\n'.format(NUM_TO_OUTPUT))
    for sub_tuple in sorted_subs_s[:NUM_TO_OUTPUT]:
        f.write('{} - {}\n'.format(sub_tuple[0], sub_tuple[1]))
    f.write('\n')

    f.write('Top {} subs by activity (comments)\n'.format(NUM_TO_OUTPUT))
    for sub_tuple in sorted_subs_c[:NUM_TO_OUTPUT]:
        f.write('{} - {}\n'.format(sub_tuple[0], sub_tuple[1]))


