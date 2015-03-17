import datetime, time
from TweetParser import *
import Features

datapath = '../data/'
outpath = '../result/'
output = 'features.csv'

class TweetStats:
	def __init__(self,hashtag):
		filename = datapath + 'tweets_#' + hashtag + '.txt'
		#filename = '../data/head.txt'
		self.parser = TweetParser(filename)
		self.tweetcount = 0
		#### Features ####
		self.frequency = list()		#Num of tweets per hour
		self.retweets = list()		#Total # of retweets per hour
		self.sumfollowers = list()	#Sum of followers per hour
		self.maxfollowers = list()	#Maximum # followers for a given tweeter
		self.time = list()
		self.timeofDay = list()

		self.followers = 0
		self.parser.load()
		self.parser.nextTweet()
		self.startTime = self.parser.getTime()

	def recordTime(self):
		time = self.parser.getTime()
		startHour = self.parser.getHour()

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

	def genVector(self):
		self.vector = [Features.NumberOfTweets(),Features.NumberOfRetweets(),Features.NumberOfFollowers(),Features.MaxFollowers(),Features.Time()]

	def genFeatures(self):
		count = 0
		outfile = open(outpath + output, 'w')
		self.genVector()
		while(True):
			time = self.parser.getTime()
			startHour = self.parser.getHour()

			index = (time - self.startTime) / 3600
			while index >= len(self.frequency):
				outfile.write(','.join([str(i) for i in self.vector]))
				self.vector = self.genVector()
			for feature in self.vector:
				feature.compute(parser.getTweet())

			if self.parser.nextTweet() is not 0:
				break
		outfile.close()	
		self.parser.close()

