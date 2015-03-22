import pymongo
from topia.termextract import extract
from textblob import TextBlob
from textblob.classifiers import NaiveBayesClassifier
import collections
import train

# Define the record tuple
#Record = collections.namedtuple ("keywords", "gender")

trainer = train.Trainer ()
trainer.load_database("train.csv", -1)

client = pymongo.MongoClient("localhost", 27017)
db = client.cs4242

extractor = extract.TermExtractor()
extractor.filter = extract.permissiveFilter

train_set = []
users =  db.users.find()

print "Processing..."
for i in range(0, users.count()):
	description = users[i]["description"]
	uid = users[i]["userId"]
	if not trainer.is_in_train(uid):
		continue
	#print uid
	keyword_list = extractor(description)
	keyword_list = [k[0] for k in keyword_list]
	keyword_str = " ".join(keyword_list)
	record = (keyword_str, trainer.get_gender_by_id(uid))
	train_set.append(record)

#print train_set

print "Training..."
classifier = NaiveBayesClassifier (train_set)

'''
print "Classifying..."
hit = 0
total = 0
for i in range(users.count()-20, users.count()):
	test_str= users[i]["description"]
	uid = users[i]["userId"]
	test_keyword_list = extractor(test_str)
	test_keyword_list = [k[0] for k in test_keyword_list]
	test_keyword_str = " ".join(test_keyword_list)
	result = classifier.classify(test_keyword_str)
	if trainer.is_in_train(uid):
		if result == trainer.get_gender_by_id(uid):
			hit+=1
		total+=1


print "correct: "+str(hit)+"/"+str(total)
'''

test_str= "19 | GatosQuesoTetasCochesCervezas | Bio sidosa | Quimico de mierda | Master en siestas"
test_keyword_list = extractor(test_str)
test_keyword_list = [k[0] for k in test_keyword_list]
test_keyword_str = " ".join(test_keyword_list)
result = classifier.classify(test_keyword_str)
print result