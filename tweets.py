import pymongo
from topia.termextract import extract
from textblob import TextBlob
from textblob.classifiers import NaiveBayesClassifier
import collections
import stopword_list
import train
import re
import time
import detect_language
import tweets_params

# Define the record tuple
#Record = collections.namedtuple ("keywords", "gender")


trainer = train.Trainer ()
trainer.load_database("train.csv", -1)
client = pymongo.MongoClient("localhost", 27017)
db = client.cs4242
extractor = extract.TermExtractor()

def tweet_to_keywords(text):
	text = re.sub(r'^https|http?:\/\/.*[\r\n]*', '', text, flags=re.MULTILINE)
	text = " ".join([word for word in text.split() if not word.startswith('@') and word not in stopword_list.get_stopwords()])
	#print text.encode("utf8")
	if tweets_params.LANGUAGE_DETECTION:
		if detect_language.detect_language(text) != "english":
			text = ""
	keyword_list = extractor(text)
	keyword_list = [k[0] for k in keyword_list]
	keyword_str = " ".join(keyword_list)
	return keyword_str

def process_tweets(tweets):
	gender_train_set = []
	age_train_set = []
	print "Processing..."
	gender_balance_count = 0
	total_train = tweets_params.TRAIN_SIZE
	if total_train > tweets.count():
		total_train = tweets.count()
	for i in range(0, total_train):
		text = tweets[i]["text"]
		uid = tweets[i]["userId"]
		if not trainer.is_in_train(uid):
			continue

		curr_gender = trainer.get_gender_by_id(uid)
		if curr_gender == "FEMALE":
			gender_balance_count-=tweets_params.TRAIN_FEMALE_RATIO
		else:
			if gender_balance_count>0:
				continue
			else:
				gender_balance_count+=tweets_params.TRAIN_MALE_RATIO
		#print curr_gender + str(gender_balance_count)
		curr_age = trainer.get_age_by_id(uid)
		#print curr_age
		#print uid
		#text = ContentNormalizer.normalize_content (text)
		keyword_str = tweet_to_keywords(text)
		if keyword_str:
			keyword_str = ' '.join(word for word in keyword_str.split() if len(word)>2)
			#print keyword_str
			gender_train_set.append((keyword_str, curr_gender))
			age_train_set.append((keyword_str, curr_age))
	return (gender_train_set, age_train_set)

def uid_to_tweets(uid):
	tweets =  db.tweets.find({ "userId": uid })
	return tweets

def train():
	extractor.filter = extract.DefaultFilter(singleStrengthMinOccur=tweets_params.KEYWORD_SENSITIVITY)

	tweets =  db.tweets.find()
	start_time = time.time()

	processed_tweets = process_tweets(tweets)
	gender_train_set = processed_tweets[0]
	age_train_set = processed_tweets[1]

	#print train_set

	print "Training tweets classifier..."
	gender_classifier = NaiveBayesClassifier (gender_train_set)
	age_classifier = NaiveBayesClassifier (age_train_set)
	print "[T] " + str(time.time() - start_time)
	return (gender_classifier, age_classifier)

def classify_user(gender_classifier, age_classifier, uid):
	u_tweets = uid_to_tweets(uid)
	gender_dict = {"MALE":0, "FEMALE":0}
	age_dict = {"18-24":0, "25-34":0, "35-49":0, "50-64":0, "65-xx":0}
	num_of_tweets = tweets_params.MAX_TWEETS_FOR_EACH_USER
	if  num_of_tweets > u_tweets.count():
		num_of_tweets = u_tweets.count()
	for i in range(0, num_of_tweets):
		t = u_tweets[i]["text"]
		t = tweet_to_keywords(t)
		if (len(t)<3):
			continue
		gender = gender_classifier.classify(t)
		gender_dict[gender]+=1
		age = age_classifier.classify(t)
		age_dict[age]+=1
	#print gender_dict
	#print age_dict
	predicted_gender = max(gender_dict, key=gender_dict.get)
	predicted_age = max(age_dict, key=age_dict.get)
	return (predicted_gender, predicted_age)