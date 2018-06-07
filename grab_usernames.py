#!./venv/bin/python3

import praw
import datetime
from os import listdir

SUB = 'Popular'
reddit = praw.Reddit('bot1')
subreddit = reddit.subreddit(SUB)

user_set = set()
num_users = 3000

output_path = '/home/pi/projects/red_connections/data/usernames/'

for submission in subreddit.stream.submissions():
	if submission.author != None:
		user_set.add(submission.author.name)

	top_level_comments = list(submission.comments)

	for comment in top_level_comments:
		if comment.author != None:
			user_set.add(comment.author.name)

	set_len = len(user_set)

	if set_len % 50 <= 1:
		print(str(set_len * 100 / num_users) + '%')

	if set_len > num_users:
		break

output_num = 0
dir_list = listdir(output_path)
dt = datetime.datetime.today()
output_filename = '{}usernames_{}_{}_{}_{}.{}.{}.txt'.format(output_path,
                                                             SUB.upper(),
                                                             num_users,
                                                             output_num,
                                                             dt.month,
                                                             dt.day,
                                                             dt.year)

while output_filename in dir_list:
    output_filename = '{}usernames_{}_{}_{}_{}.{}.{}.txt'.format(output_path,
                                                                 SUB.upper(),
                                                                 num_users,
                                                                 output_num + 1,
                                                                 dt.month,
                                                                 dt.day,
                                                                 dt.year)

with open(output_filename, 'w') as f:
	for username in user_set:
		f.write(username + '\n')

