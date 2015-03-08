import datetime, time
from TweetParser import *

datapath = '../data/'
outpath = '../result/'

class TweetStats:
	def __init__(self,hashtag):
		filename = datapath + 'tweets_#' + hashtag + '.txt'
		#filename = '../data/head.txt'
		self.parser = TweetParser(filename)
		self.tweetcount = 0
		self.frequency = list()
		self.followers = 0
		self.parser.load()
		self.parser.nextTweet()
		self.startTime = self.parser.getTime()

	def recordTime(self):
		time = self.parser.getTime()
		#print time
		index = (time - self.startTime) / 3600
		while index >= len(self.frequency):
			self.frequency.append(0)

		self.frequency[index] += 1

	def countFollowers(self):
		#print self.parser.getFollowerCount()
		self.followers += self.parser.getFollowerCount()

	def compute(self):
		while True:
			self.recordTime()
			self.countFollowers()
			self.tweetcount += 1
		#	print 'tweetcount' + str(self.tweetcount)
			if self.parser.nextTweet() is not 0:
				break
		self.parser.close()
	
	def averageFollowerCount(self):
		return self.followers*1.0/self.tweetcount

	def writeTweetFrequency(self, output):
		outfile = open(outpath + output, 'w')
		i = 0
		for item in self.frequency:
			line = str(i) + ',' + str(item) + '\n'
			outfile.write(line)
			i += 1
		outfile.close()
