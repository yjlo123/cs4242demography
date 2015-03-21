import sys
import csv
import pymongo
from params import *
from namedtuple import *
from checkin_classifier import CheckInClassifier

def extractUserData ():
	### Load user data from the train data file into memory
	f_input = open (USER_DATA_FILE, 'rt')
	reader = csv.reader (f_input)
	next (reader)

	user_data = []
	for row in reader:
		# Extract feature
		userId = row[0]
		gender = row[1]
		ageGroup = row[2]
		user = User (userId, gender, ageGroup)

		# Add the information to user data
		user_data.append (user)

	f_input.close ()
	return user_data

def extractFeatureFromEntry (entry, user_data):
	# Extract feature from entry
	userId = entry["userId"]
	user = None
	for curr in user_data:
		if curr.userId == userId:
			user = curr
			break
	if "venue" in entry.keys():
		location = entry["venue"]["location"]
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
	else:
		location = None
	feature = CheckInFeature (user, location)
	return feature

def getTrainData ():
	### retrieve database from host
	client = pymongo.MongoClient (MONGO_HOST, MONGO_PORT)
	users_db = client.cs4242.users
	checkins_db = client.cs4242.checkins

	### Constants
	DATA_COUNT = checkins_db.count ()							### number of entry in the database
	USER_COUNT = users_db.count ()								### number of user in the database
	LOWER_ID = DATA_COUNT / FOLD_COUNT * TEST_FOLD				### the lower id bound of the test fold
	UPPER_ID = DATA_COUNT / FOLD_COUNT * (TEST_FOLD + 1)		### the upper id bound of the test fold

	user_data = extractUserData ()

	### load the data from the database into memory
	train_data = []
	for i in range (0, DATA_COUNT):
		# Check whether the data is in the test fold
		# If yes, do not process
		if i in range (LOWER_ID, UPPER_ID):
			continue

		# Extract feature from the i-th entry and add to the train_data
		entry = checkins_db.find ()[i]
		feature = extractFeatureFromEntry (entry, user_data)
		train_data.append (feature)

	return train_data

def getTestData ():
	### retrieve database from host
	client = pymongo.MongoClient (MONGO_HOST, MONGO_PORT)
	users_db = client.cs4242.users
	checkins_db = client.cs4242.checkins

	### Constants
	DATA_COUNT = checkins_db.count ()							### number of entry in the database
	USER_COUNT = users_db.count ()								### number of user in the database
	LOWER_ID = DATA_COUNT / FOLD_COUNT * TEST_FOLD				### the lower id bound of the test fold
	UPPER_ID = DATA_COUNT / FOLD_COUNT * (TEST_FOLD + 1)		### the upper id bound of the test fold

	user_data = extractUserData ()

	### load the data from the database into memory
	test_data = []
	for i in range (0, DATA_COUNT):
		# Check whether the data is in the test fold
		# If no, do not process
		if i not in range (LOWER_ID, UPPER_ID):
			continue

		# Extract feature from the i-th entry and add to the test_data
		entry = checkins_db.find ()[i]
		feature = extractFeatureFromEntry (entry, user_data)
		test_data.append (feature)

	return test_data