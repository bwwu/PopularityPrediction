from TweetStats import *
from Feature import Feature
import Regression
import statsmodels

hashtag_list = ['gohawks', 'nfl', 'superbowl', 'gopatriots', 
'patriots','sb49']

features = ['NumberOfTweets','NumberOfRetweets', 'NumberOfFollowers','MaxFollowers','Time']
predictant = ['NumberOfTweets']

m = Regression.ModelBuilder(features, predictant)

for tag in hashtag_list:
	
	tp = TweetStats(tag)
	filename = 'pt2_' + tag + '.csv'
	tp.genFeatures(filename)
	print 'Feature extraction done for' + tag + '.........'	
	m.open(filename)
	model = m.model()
	print model.fit().summary()
	