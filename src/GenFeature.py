import datetime, time
from TweetParser import *
import Feature

datapath = '../data/samples/'
outpath = '../result/'

startTime = 1419804000


features = [ 'Index', 'NumberOfTweets', 'NumberOfRetweets', 
				'NumberOfFollowers', 'MaxFollowers',
				'Time']

class GenFeature:
	def __init__(self,hashtag, filename):
		# hash tag
		self.hashtag = hashtag
		self.filename=filename
		#filename = datapath + 'tweets_#' + hashtag + '.txt'
		#filename = '../data/head.txt'
		self.parser = TweetParser(datapath + filename)
		self.tweetcount = 0
		#### Features ####
		self.frequency = list()		#Num of tweets per hour

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

	def genFeatures(self):
		output = 'pt5_' + self.filename
		outfile = open(outpath + output, 'w')

		outfile.write(','.join(features)+'\n') #csv headers

		self.count = 0
		self.genVector() # initial hour


		numT = 0
		while(True): 
			time = self.parser.getTime()
			index = (time - startTime) / 3600 # calculate current hour

			while index >= self.count: # new hour
				# write prev hour features to csv
				if numT is 0: 
					break
				outfile.write(','.join(map(str,[self.count] + [a.get() for a in self.vector]))+'\n')
				self.genVector() # for new hour
				numT = 0
				self.count += 1
			
			for f in self.vector: # recompute features 
				f.compute(self.parser.getTweet())
				numT += 1

			if self.parser.nextTweet() is not 0: # grab next tweet
				break

		outfile.close()	
		self.parser.close()
