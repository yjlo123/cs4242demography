import pymongo
from topia.termextract import extract
from textblob import TextBlob
from textblob.classifiers import NaiveBayesClassifier
import collections
import train

out_result = open("M-3-3.txt", 'w')
out_result2 = open("F-3-3.txt", 'w')
trainer = train.Trainer ()
trainer.load_database("train.csv", -1)
client = pymongo.MongoClient("localhost", 27017)
db = client.cs4242

extractor = extract.TermExtractor()
extractor.filter = extract.DefaultFilter(singleStrengthMinOccur=2)

tweets =  db.tweets.find()

print "Processing..."
for i in range(tweets.count()*2/3, tweets.count()):
	text = tweets[i]["text"]
	uid = tweets[i]["userId"]
	if not trainer.is_in_train(uid):
		continue
	if (trainer.get_gender_by_id(uid) == "MALE"):
		out_result.write(" "+text.encode('utf8'))
	elif (trainer.get_gender_by_id(uid) == "FEMALE"):
		out_result2.write(" "+text.encode('utf8'))

	if(i%500 == 0):
		print str(i/500)+"/"+str(tweets.count()/500)

out_result.close()
