#!./venv/bin/python3

import praw

SUB = 'All'
reddit = praw.Reddit('bot1')
subreddit = reddit.subreddit(SUB)

user_set = set()
num_users = 10000

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

with open('usernames_' + SUB.upper() + '_' + str(num_users) + '.txt', 'w') as f:
	for username in user_set:
		f.write(username + '\n')

