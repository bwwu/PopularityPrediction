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
	def __init__(self, features, predictant):
		self.formula = '+'.join(predictant) + '~' + '+'.join(features)
		self.df = None

	def open(self,csvfile):
		self.df = pandas.read_csv(datapath + csvfile)
	
	def model(self):
		return smf.ols(formula=self.formula, data=self.df)

