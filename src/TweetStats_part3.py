import datetime, time
from TweetParser import *
import Feature

datapath = '../data/'
outpath = '../result/'
#output = 'features.csv'

startTime = 1419804000


features = [ 'Index', 'NumberOfTweets', 'NumberOfRetweets', 
				'NumberOfFollowers', 'MaxFollowers',
				'Time']

features = [
	'Index',
	'NumberOfTweets',
    'URLRatio',
    'AuthorCount',
    'NumberOfRetweets']

class TweetStats:
	def __init__(self,hashtag):
		# hash tag
		self.hashtag = hashtag

		filename = datapath + 'tweets_#' + hashtag + '.txt'
		#filename = '../data/head.txt'
		self.parser = TweetParser(filename)
		self.tweetcount = 0
		#### Features ####
		self.frequency = list()		#Num of tweets per hour
#		self.retweets = list()		#Total # of retweets per hour
#		self.sumfollowers = list()	#Sum of followers per hour
#		self.maxfollowers = list()	#Maximum # followers for a given tweeter
#		self.time = list()
#		self.timeofDay = list()

		self.followers = 0
		self.parser.load()
		self.parser.nextTweet()
		self.startTime = self.parser.getTime()
		self.vector = list()
		self.count = 0	# number of hours

	def recordTime(self):
		time = self.parser.getTime()
		startHour = self.parser.getHour()

		index = (time - self.startTime) / 3600
		while index >= len(self.frequency):
			self.frequency.append(0)

		self.frequency[index] += 1

	def countFollowers(self):
		self.followers += self.parser.getFollowerCount()

	def compute(self):
		while True:
			self.recordTime()
			self.countFollowers()
			self.tweetcount += 1
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

	def genVector(self): # new feature vector for new hour
		hour = (self.count + time.localtime(startTime).tm_hour) % 24
		self.vector = [Feature.NumberOfTweets(),Feature.NumberOfRetweets(),
		Feature.NumberOfFollowers(),Feature.MaxFollowers(),Feature.Time(hour)]
		
		self.vector = [Feature.NumberOfTweets(),Feature.URLRatio(), Feature.AuthorCount(), Feature.NumberOfRetweets()]

	def genFeatures(self):
		output = 'pt3_' + self.hashtag + '.csv'
		outfile = open(outpath + output, 'w')

		outfile.write(','.join(features)+'\n') #csv headers

		self.count = 0
		self.genVector() # initial hour
		while(True):
			time = self.parser.getTime()
			index = (time - startTime) / 3600 # calculate current hour

			while index >= self.count: # new hour
				# write prev hour features to csv
				outfile.write(','.join(map(str,[self.count] + [a.get() for a in self.vector]))+'\n')
				self.genVector() # for new hour
				self.count += 1
			
			for f in self.vector: # recompute features 
				f.compute(self.parser.getTweet())

			if self.parser.nextTweet() is not 0: # grab next tweet
				break

		outfile.close()	
		self.parser.close()


class FeatureGen:
	def __init__(self, hashtag):
		filename = datapath + 'tweets_#' + hashtag + '.txt'	# Filename
		# Member data
		self.hashtag = hashtag
		self.parser = TweetParser(filename)
		self.fvector = None		# Feature vector	[F1, F2, F3, ...]
		self.output = None
		
	# Creates vector of updateable features
	def vector(self):
		self.fvector = [Feature.NumberOfTweets(),Feature.NumberOfRetweets(),
		Feature.NumberOfFollowers(),Feature.MaxFollowers(),Feature.Time(0)]

	# Build feature matrix for all data
	def generate(self):
		output = 'feature_' + self.hashtag + '.csv'
		self.output = output

		outfile = open(outpath + output, 'w')
		values = list()

		outfile.write(','.join(features)+'\n')

		self.vector()

		self.parser.load()
		while(self.parser.nextTweet() is not 0):

			time = self.parser.getTime()
			index = (time - startTime) / 3600
			
			# Write out features for current index
			while index >= count:
				outfile.write(','.join(map(str,[count] + 
				[a.get() for a in self.vector]))+'\n')
				self.vector()
				self.count += 1
			
			for f in self.vector:
				f.compute(self.parser.getTweet())

		outfile.close()	
		self.parser.close()
	
	def outfile(self):
		return self.output
