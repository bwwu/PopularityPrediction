from TweetStats import *
import Regression
import random

hashtag_list = ['gohawks', 'nfl', 'superbowl', 'gopatriots', 
'patriots','sb49']

datapath = '../data/'
outpath = '../result/'

features = [
	'NumberOfTweets',
	'NumberOfRetweets',
	'NumberOfFollowers', 
	'MaxFollowers',
	'Time']

predictant = ['NumberOfTweets']
response = 'NumberOfTweets'



for tag in hashtag_list:

	m = Regression.ModelBuilder(features, predictant)	
	m.open('pt2_' + tag + '.csv')
	mod = m.model()
		
	length = m.length()
	ts_size = length/10	# size of training set
	idx_arr = random.sample(range(length), length)

	avg_err = 0
	for i in range(10):
		iarr = idx_arr[i*ts_size:(i+1)*ts_size]
		m.makeTrainingSet(iarr)
		avg_err += m.crossvalidation()
		
	avg_err = avg_err/10
	print tag + ' avg error = ' + str(avg_err)
