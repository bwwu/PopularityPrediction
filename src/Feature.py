import datetime, time
from TweetParser import *
from TweetStats import *
from abc import ABCMeta, abstractmethod

datapath = '../data/'
outpath = '../result/'

class Feature:
	@abstractmethod
	def compute(self,tweet):
		pass

class NumberOfTweets(Feature):
	def __init__(self):
		self.tweetcount = 0

	def compute(self,tweet):
		self.tweetcount += 1
		return self.tweetcount

class NumberOfRetweets(Feature):
	def __init__(self):
		self.retweet = 0

	def compute(self,tweet):
		self.retweet += tweet['metrics']['citations']['data'][0]['citations']
		return self.retweet

class NumberOfFollowers(Feature):
	def __init__(self):
		self.followers = 0

	def compute(self,tweet):
		self.followers += tweet['tweet']['user']['followers_count']
		return self.followers

class MaxFollowers(Feature):
	def __init__(self):
		self.max = 0

	def compute(self,tweet):
		curr = tweet['tweet']['user']['followers_count']
		if(curr > self.max):
			self.max = curr
		return self.max

class Time(Feature):
	def compute(self,tweet):
		return tweet['firstpost_date']