import TweetStats		#for startTime
import statsmodels.formula.api as smf
import numpy as np
import pandas
from patsy import dmatrices

datapath = '../result/'

features = [
	'Time',
	'MaxFollowers',
	'NumberOfFollowers', 
	'NumberOfRetweets',
	'NumberOfTweets'
]

predictant = ['NumberOfTweets']
response = 'NumberOfTweets'

class ModelBuilder:
	def __init__(self, features, response):

		self.features = features	# Arr of Features to bld model
		self.resp = response			# Response var (predictant)

		self.df = None
		self.train_s = None
		self.test_s = None

	def open(self,csvfile):
		self.df = pandas.read_csv(datapath + csvfile)
		# Fix dataset to include next hour's tweet count
		
	def model(self):
		#TODO: replace response with member var
		formula =  response +'~' + '+'.join(self.features)
		y,X = dmatrices(formula, data=self.df, return_type="dataframe")
		y = y.shift(-1)
		return smf.OLS(y[0:-1],X[0:-1])
		

	# Make training and testing set based off array of indices
	def makeTrainingSet(self, idxarr):

		dtrain = dict()
		dtest = dict()

		# Select all indices not in the training set for test set
		test_idx = [i for i in range(len(self.df)) if i not in idxarr]

		for f in features:
			arr = self.df[f].values.tolist()	#Change each frame column to list
			a_train = [arr[i] for i in idxarr]	# Select elm i for i in idxarr
			a_test = [arr[i] for i in test_idx]	# elm i for i not in idxarr
			
			dtrain.update({f : a_train})
			dtest.update({f : a_test})

		self.train_s = pandas.DataFrame(dtrain)
		self.test_s = pandas.DataFrame(dtest)
	
	# Given a dataframe select rows within specified time frame
	def prune(self, t_init, t_final):
		t_start = TweetStats.startTime
		idx_init = 0 if t_init is 0 else (t_init - t_start)/3600
		idx_final = len(self.df) if t_final is 0 else (t_final - t_start)/3600
		
		df = self.df.shift(-idx_init)
		self.df = df[0:idx_final-idx_init]

	#
	def crossvalidation(self):
	#	print 'Cross validation....'
		formula =  response +'~' + '+'.join(features)
		#print '*****************'
		#print formula
		y,X = dmatrices(formula, data=self.train_s, return_type="dataframe")
		mod = smf.OLS(y,X)
		res = mod.fit()

		resid = 0			# Sum of |y_exp - y_pred|
		df = self.test_s	# Testing set

		#TODO: replace response with member data
		for i in range(len(df)-1):		# For each data point in testing set
			dexog = df.loc[i].to_dict()	# Vector of features

			texog = df.loc[i].tolist()	# Vector of features
			#texog['Intercept'] = 1
			texog.insert(0,1)
			#print X[:-5]

			#print texog
			#print dexog

			ypred = res.predict(exog=texog)	# Prediction
			ypred = ypred[0]
			yexp = df[response].loc[i+1]
			resid += abs(ypred - yexp)	

		avg_e =  resid*1.0/(len(df)-1)	# Avg prediction error
		#print avg_e
		return avg_e


	def length(self):
		if self.df is None:
			return -1
		return len(self.df)

	def dataframe(self):
		return self.df
