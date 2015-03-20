import pymongo
from collections import namedtuple

### retrieve database from host
client = pymongo.MongoClient (host = "localhost", port = 27017)
users_db = client.cs4242.users
checkins_db = client.cs4242.checkins

### Constants
TEST_FOLD = 0											### the fold id to test, will not load this fold when trainning
FOLD_COUNT = 10											### number of fold to split the database
DATA_COUNT = checkins_db.count ()						### number of entry in the database
LOWER_ID = DATA_COUNT / FOLD_COUNT * TEST_FOLD			### the lower id bound of the test fold
UPPER_ID = DATA_COUNT / FOLD_COUNT * (TEST_FOLD + 1)	### the upper id bound of the test fold

### Define namedtuple
Location = namedtuple ("Location", ["latitude", "longidute"])
CheckInFeature = namedtuple ("CheckInFeature", ["userId", "location"])

### load the data from the database into memory
test_data = []

for i in range (0, DATA_COUNT):
	# Check whether the data is in the test fold
	# If yes, do not process
	if i in range (LOWER_ID, UPPER_ID):
		continue

	# Get the i-th entry
	data = checkins_db.find ()[i]			### Should cache the checkins_db.find () ?

	# Extract feature from entry
	userId = data["userId"]
	if "venue" in data.keys():
		venue = data["venue"]
		latitude = venue["location"]["lat"]
		longidute = venue["location"]["lng"]
		location = Location (latitude, longidute)
	else:
		location = None
	features = CheckInFeature (userId, location)

	# Append feature to the list of data to train
	test_data.append (features)

