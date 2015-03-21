from params import *
from namedtuple import *
from checkin_classifier import CheckInClassifier
import data_getter

# Load up both train data and test data
train_data = data_getter.getTrainData ()
test_data = data_getter.getTestData ()

# Create the classifiers and train them with the data
ageClassifier = CheckInClassifier ("ageGroup", radius = 200)
genderClassifier = CheckInClassifier ("gender", radius = 600)
ageClassifier.train_classifier (train_data)
genderClassifier.train_classifier (train_data)

ageHit = 0
genderHit = 0
total = len (test_data)
for test in test_data:
	# Skip the incomplete entry
	if test.user == None or test.location == None:
		continue

	# Get classify result
	result = User (None, genderClassifier.classify (test.location).result, ageClassifier.classify (test.location).result)

	# Compare with known result
	if result.ageGroup == test.user.ageGroup:
		ageHit += 1
	if result.gender == test.user.gender:
		genderHit += 1

print "Total test:", total
print "---------------------------------------------"
print "Correct gender guess:", genderHit
print "Wrong gender guess:", total - genderHit
print "Correct %:", float (genderHit) / total * 100.0
print "---------------------------------------------"
print "Correct age guess:", ageHit
print "Wrong age guess:", total - ageHit
print "Correct %:", float (ageHit) / total * 100.0