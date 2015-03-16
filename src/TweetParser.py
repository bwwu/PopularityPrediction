import json
import datetime, time
#from TweetGrabber import *

class TweetParser:
	def __init__(self, filename):		# Open a tweet JSON file for parsing
		self.filename = filename	
		self.fh	= None
		self.tweet = None
		self.hashtags = []
	
	def load(self):
		self.fh = open(self.filename, 'r')

	def close(self):
		if self.fh is None:
			print 'Error! No file is open'
			return
		self.fh.close()
		self.fh = None

	def nextTweet(self):					# Parse next tweet in file
		if self.fh is None:
			print 'Error! No file is open'
			return -1
		line = self.fh.readline()
		if not line:
			self.tweet = None
			self.hashtags = None
			return -1	
		self.tweet = json.loads(line)
		#print self.tweet['tweet']['entities']['hashtags']
		self.hashtags = []
		self.parseHashtags()
		return 0

	def getTime(self):
		return self.tweet['firstpost_date']
	
	def hasTag(self, hashtag):
		for tag in self.hashtags:
			if hashtag == tag:
				return True
		return False

	def parseHashtags(self):		
		tags = self.tweet['tweet']['entities']['hashtags']
		for i in range(len(tags)):
			tag = tags[i]['text']
			self.hashtags.append(tag.upper())
			#print tags[i]['text']

	def getFollowerCount(self):
		return self.tweet['tweet']['user']['followers_count']

	def getRetweetCount(self):
		return self.tweet['metrics']['citations']['data'][0]['citations']
	
	def getHour(self):
		tm = self.getTime()
		tt = time.localtime(tm)
		return tt.tm_hour

	def getHashtags(self):			# Return a list of hashtags 
		return self.hashtags

	def getTweet(self):				# Return full tweet data
		return self.tweet
