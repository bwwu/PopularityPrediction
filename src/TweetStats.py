import datetime, time
from TweetParser import *
import Feature

datapath = '../data/'
outpath = '../result/'
output = 'features.csv'

class TweetStats:
	def __init__(self,hashtag):
		filename = datapath + 'split_tweets_#' + hashtag + '.txt'
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
		self.vector = list()

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
		self.vector = [Feature.NumberOfTweets().compute(self.parser.getTweet()),Feature.NumberOfRetweets().compute(self.parser.getTweet()),Feature.NumberOfFollowers().compute(self.parser.getTweet()),Feature.MaxFollowers().compute(self.parser.getTweet()),Feature.Time().compute(self.parser.getTweet())]

	def genFeatures(self):
		count = 0
		outfile = open(outpath + output, 'w')
		values = list()
		index = 0
		while(True):
			self.genVector()
			time = self.parser.getTime()
			temp = index
			index = (time - self.startTime) / 3600
			
			if(temp > index):
				print "This should never print out..."

			try:
			    temp = values[index]
			    values[index] = self.vector
			except IndexError:
			    values.append(self.vector)

			if self.parser.nextTweet() is not 0:
				break

		for w in range(0,len(values)-1,1):
			outfile.write(str(w) + ',' + ','.join(map(str, values[w])) + '\n')

		outfile.close()	
		self.parser.close()