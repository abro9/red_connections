#!./venv/bin/python3

from os import listdir

user_set = set()

input_path = '/home/pi/projects/red_connections/data/usernames/'
output_path = '/home/pi/projects/red_connections/data/all_usernames.txt'

dir_list = listdir(input_path)

for user_file in dir_list:
    current_input_file = '/home/pi/projects/red_connections/data/usernames/{}'.format(user_file)
    
    with open(current_input_file, 'r') as f:
        for line in f:
            user_set.add(line)

with open(output_path, 'w') as f:
	for username in user_set:
		f.write(username)

