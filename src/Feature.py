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
	def __init__(self):
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
	
class URLRatio(Feature):
	def __init__(self):
		self.urlRatio = 0
		self.tweetCount = 0
	
	def compute(self,tweet):		
		urls = tweet['tweet']['entities']['urls']
		numberOfURLsInTweet = len(urls)
		self.urlRatio += numberOfURLsInTweet
		self.tweetCount += 1
		return self.urlRatio
	
	def get(self):
		if self.tweetCount == 0:
			return 0
		return self.urlRatio*1.0/self.tweetCount

class FriendCount(Feature):#Average Friend Count for Each Unique User
	def __init__ (self):
		self.friendCount = 0
		self.authorCount = 0
		self.authorDict = {}
		
	def compute(self,tweet):
		authorID = tweet['tweet']['user']['id']
		if(not self.authorDict.has_key(authorID)):			
			self.authorDict[authorID] = 1
			self.authorCount += 1
			self.friendCount += tweet['tweet']['user']['friends_count']
		
	def get(self):
		if self.authorCount == 0:
			return 0
		return self.friendCount/self.authorCount
	
class AuthorCount(Feature):
	def __init__ (self):
		self.authorCount = 0
		self.authorDict = {}
		
	def compute(self,tweet):
		authorID = tweet['tweet']['user']['id']
		if(not self.authorDict.has_key(authorID)):			
			self.authorDict[authorID] = 1
			self.authorCount += 1
		
	def get(self):		
		return self.authorCount
	
class MeanOfRetweets(Feature):
	def __init__(self):
		self.mean = 0
		self.retweetCount = 0
		self.tweetCount = 0
		
	def compute(self,tweet):
		self.retweetCount += tweet['metrics']['citations']['data'][0]['citations']
		self.tweetCount += 1 
		return self.retweetCount
	
	def get(self):
		if self.tweetCount == 0:
			return 0
		return self.retweetCount/self.tweetCount
	
	
		