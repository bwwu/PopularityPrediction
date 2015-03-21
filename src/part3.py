from TweetStats import *
import Regression

hashtag_list = ['gohawks', 'nfl', 'superbowl', 'gopatriots', 
'patriots','sb49']

features = [
    'URLRatio',
    'AuthorCount',
    'NumberOfRetweets']

predictant = ['NumberOfTweets']
response = 'NumberOfTweets'

m = Regression.ModelBuilder(features, predictant)

for tag in hashtag_list:
    tp = TweetStats(tag)
    tp.genFeatures()
    print 'Feature extraction done for' + tag + '.........'
    filename = 'pt3_' + tag + '.csv'
    m.open(filename)
    model,X = m.model()
    predictions = model.fit().predict()
    content = ""
    X = X[0:-1]
    output = 'pt3_Predictions_' + tag + '.csv'
    outfile = open(outpath + output, 'w')
    content += "PredictedNumberOfTweets" +"," +"Intercepts"+","+(','.join(map(str,features))+"\n")
    for i in range(len(predictions)):
        content += str(predictions[i])+","+(','.join(map(str,X.loc[i].tolist()))+"\n")
        
        
    outfile.write(content)
    outfile.close()

