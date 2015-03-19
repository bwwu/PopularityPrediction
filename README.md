##Current Bugs
* FeatureGen outputs a BS row in the first line (see repeated hour value)

##Latest Fixes
* Hours that contain no tweets have appropriate value for time of day (24hr)
* Added functionality to create train/test set via list of indices

##Todo
* Add new features for Part 3 in Feature.py
* Clean up TweetStats.py modules (separate FeatureGen and Part 1 stats)
* Prune DataFrame based on time window (for Part 4) e.g date < Feb 1st
