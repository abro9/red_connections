#!./venv/bin/python3

import praw
import os import listdir

SUB = 'All'
reddit = praw.Reddit('bot1')
subreddit = reddit.subreddit(SUB)

user_set = set()
num_users = 2000

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
dir_list = listdir('./')
output_filename = 'usernames_{}_{}_{}.txt'.format(SUB.upper(), num_users, output_num)

while output_filename in dir_list:
    output_filename = 'usernames_{}_{}_{}.txt'.format(SUB.upper(), num_users, output_num + 1)

with open(output_filename, 'w') as f:
	for username in user_set:
		f.write(username + '\n')

