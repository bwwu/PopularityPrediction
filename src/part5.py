import random, datetime, time
import Regression
import GenFeature as gf

samplePath = '../data/samples/'

sfiles = [	
	['sample1_period1.txt',
	'sample4_period1.txt',
	'sample5_period1.txt',
	'sample8_period1.txt'],
	['sample2_period2.txt',
	'sample6_period2.txt',
	'sample9_period2.txt'],
	['sample10_period3.txt',
	'sample3_period3.txt',
	'sample7_period3.txt'] ] 

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
#####################
# Start of script 
#####################

for i in range(len(window_start)):
	for f in sfiles[i]:
		feat = gf.GenFeature("",f)
		feat.genFeatures()

print 'DONE~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~'

for i in range(len(window_start)):
	m = Regression.ModelBuilder(features, predictant)
	m.open('pt2_superbowl.csv')
	m.prune(window_start[i],window_end[i])	
	
	model = m.model()
	res = model.fit()
	
	for f in sfiles[i]:

		print 'Info for ' + f

		# Build a feature set for tweets in f
		#feat = gf.GenFeature("",f)
		#feat.genFeatures()
	
		# Open a data frame for tweets in f
		test_set = Regression.ModelBuilder(features, predictant)
		test_set.open('pt5_'+f)
		
		test_df = test_set.dataframe()
		
		# Compute prediction for tweets in data frame
		for k in range(len(test_df)):
			x = test_df.loc[k].tolist()
			#x.insert(0,1)
			ypred = res.predict(exog=x)
			ypred = ypred[0]
		
			print str(test_df['Index'][k]) + ',' + str(abs(ypred))
