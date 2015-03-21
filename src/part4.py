import random, datetime, time
import Regression
from TweetStats import *
#######################################
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
#########################################
window_start = [
	0,
	int(time.mktime(((datetime.datetime(2015,02,01,8,00,0)).timetuple()))),
	int(time.mktime(((datetime.datetime(2015,01,14,12,30,0)).timetuple())))
]

window_end = [
	int(time.mktime(((datetime.datetime(2015,02,01,8,00,0)).timetuple()))),
	int(time.mktime(((datetime.datetime(2015,02,01,20,00,0)).timetuple()))),
	0
]


for j in range(len(window_start)):
	print '*****************************' 
	for tag in hashtag_list:
	
		m = Regression.ModelBuilder(features, predictant)	
		m.open('pt2_' + tag + '.csv')
		mod = m.model()
		
		#print window_start[j]
		#print window_end[j]
		m.prune(window_start[j],window_end[j])

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
