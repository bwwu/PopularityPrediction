from TweetStats import *

hashtag_list = ['gohawks', 'nfl', 'superbowl', 'gopatriots', 'sb49']

print 'hashtag -- Average Follower count'
for tag in hashtag_list:
	tp = TweetStats(tag)
	tp.compute()
	line = tag + ' -- ' + str(tp.averageFollowerCount())
	print line
	tp.writeTweetFrequency(tag + '.csv')
