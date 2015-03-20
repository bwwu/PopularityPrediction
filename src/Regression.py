import sys
import TweetStats		#for startTime
import statsmodels.formula.api as smf
import numpy as np
import pandas

datapath = '../result/'

if __name__ == '__main__':
	dataset = '../data/test.csv'	#Feature set

	df = pandas.read_csv(dataset)
	model = smf.ols(formula='numTweets ~ totalRetweets + sumFollowers + maxFollowers + timeOfDay', data=df)


features = ['NumberOfRetweets', 'NumberOfFollowers', 'MaxFollowers',
				'Time']
predictant = ['NumberOfTweets']

class ModelBuilder:
	def __init__(self, features, response):
		self.formula = '+'.join(response) + '~' + '+'.join(features)
		self.df = None
		self.train_s = None
		self.test_s = None

	def open(self,csvfile):
		self.df = pandas.read_csv(datapath + csvfile)
		# Fix dataset to include next hour's tweet count
		
	def model(self):
		return smf.ols(formula=self.formula, data=self.df)

	# Make training and testing set based off array of indices
	def makeTrainingSet(self, idxarr):

		dtrain = dict()
		dtest = dict()

		# Select all indices not in the training set for test set
		test_idx = [i for i in range(len(self.df) if i not in idxarr)]

		for f in features:
			arr = self.df[f].values.tolist()	#Change each frame column to list
			a_train = [arr[i] for i in idxarr]	# Select elm i for i in idxarr
			a_test = [arr[i] for i in test_idx]	# elm i for i not in idxarr
			
			dtrain.update({f : a_train})
			dtest.update({f : a_test})

		self.train_s = DataFrame(dtrain)
		self.test_s = DataFrame(dtest)
	
	# Given a dataframe select rows within specified time frame
	def prune(self, t_init, t_final):
		t_start = TweetStats.startTime
		idx_init = 0 if t_init is 0 else (t_init - t_start)/3600
		idx_final = len(df) if t_final is 0 else (t_final - t_start)/3600
		
		df = df[idx_init:idx_final]


	#def crossvalidation:
		
