from TweetStats import *
import Regression

hashtag_list = ['gohawks', 'nfl', 'superbowl', 'gopatriots', 
'patriots','sb49']

features = [
	'NumberOfTweets',
	'NumberOfRetweets',
	'NumberOfFollowers', 
	'MaxFollowers',
	'Time']

predictant = ['NumberOfTweets']
response = 'NumberOfTweets'

m = Regression.ModelBuilder(features, predictant)

for tag in hashtag_list:
#	tp = TweetStats(tag)
#	tp.genFeatures()
	print 'Feature extraction done for' + tag + '.........'
	filename = 'pt2_' + tag + '.csv'
	m.open(filename)
	model = m.model()
	print model.fit().summary()

