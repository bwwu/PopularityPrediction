import datetime, time
from TweetParser import *
from TweetStats import *

datapath = '../data/'
outpath = '../result/'

class Feature:
	@abstractmethod
	def compute(self,tweet):
		pass


class NumberOfTweets(Features):
	def compute(self,tweet):
		self.tweetcount += 1
		return self.tweetcount

class NumberOfRetweets(Features):
	def compute(self,tweet):
		self.retweet += tweet['metrics']['citations']['data'][0]['citations']
		return self.retweet

class NumberOfFollowers(Features):
	def compute(self,tweet):
		self.followers += tweet['tweet']['user']['followers_count']
		return self.followers

class MaxFollowers(Features):
	def compute(self,tweet):
		self.max = 0
		curr = tweet['tweet']['user']['followers_count']
		if(curr > self.max):
			self.max = curr
		return self.max

class Time(Features):
	def compute(self,tweet):
		return tweet['firstpost_date']