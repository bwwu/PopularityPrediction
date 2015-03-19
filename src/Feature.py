import datetime, time
from TweetParser import *
from TweetStats import *
from abc import ABCMeta, abstractmethod

datapath = '../data/'
outpath = '../result/'

class Feature: # base Feature class 
	@abstractmethod
	def compute(self,tweet): # abstract method for feature extraction
		pass
	@abstractmethod
	def get(self):
		pass

class NumberOfTweets(Feature): # returns current tweet count
	def __init__(self):
		self.tweetcount = 0

	def compute(self,tweet):
		self.tweetcount += 1 
		return self.tweetcount
	def get(self):
		return self.tweetcount

class NumberOfRetweets(Feature): # returns current retweet count
		self.retweet = 0

	def compute(self,tweet):
		self.retweet += tweet['metrics']['citations']['data'][0]['citations'] 
		return self.retweet
	def get(self):
		return self.retweet

class NumberOfFollowers(Feature): # returns total follower count
	def __init__(self):
		self.followers = 0

	def compute(self,tweet):
		self.followers += tweet['tweet']['user']['followers_count'] 
		return self.followers
	def get(self):
		return self.followers

class MaxFollowers(Feature): # returns max follower count of all tweets
	def __init__(self):
		self.max = 0

	def compute(self,tweet):
		curr = tweet['tweet']['user']['followers_count']
		if(curr > self.max): 
			self.max = curr
		return self.max
	def get(self):
		return self.max

class Time(Feature): # returns hour value of tweet's post date 
	def __init__(self,hour):
		self.hour = hour

	def compute(self,tweet):
		temp = tweet['firstpost_date']
		temp = time.localtime(temp)
		self.hour = temp.tm_hour
	def get(self):
		return self.hour
