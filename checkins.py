import pymongo
from checkins_classsifier import checkin
from checkins_classsifier.namedtuple import *

client = pymongo.MongoClient("localhost", 27017)
db = client.cs4242

def predict_by_checkin(uid):
	checkins =  db.checkins.find({ "userId": uid })
	gender_dict = {"MALE":0, "FEMALE":0}
	age_dict = {"18-24":0, "25-34":0, "35-49":0, "50-64":0, "65-xx":0}
	num_of_checkin = checkins.count()
	if (num_of_checkin>10):
		num_of_checkin = 10
	for i in range(0, num_of_checkin):
		location = checkins[i]["venue"]["location"]
		latitude = location["lat"]
		longidute = location["lng"]
		if "address" in location.keys():
			address = location["address"]
		else:
			address = None
		if "context" in location.keys():
			context = location["context"]
		else:
			context = None
		location = Location (address, context, latitude, longidute)
		gender = checkin.classify(location).gender
		age = checkin.classify(location).ageGroup
		gender_dict[gender]+=1
		age_dict[age]+=1
	predicted_gender = max(gender_dict, key=gender_dict.get)
	predicted_age = max(age_dict, key=age_dict.get)
	return (predicted_gender, predicted_age)