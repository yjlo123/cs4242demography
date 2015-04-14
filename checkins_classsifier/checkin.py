from params import *
from namedtuple import *
from checkin_classifier import CheckInClassifier
import data_getter

# Load up both train data and test data
train_data = data_getter.getTrainData ()

# Create the classifiers and train them with the data
ageClassifier = CheckInClassifier ("ageGroup", radius = 200)
genderClassifier = CheckInClassifier ("gender", radius = 600)
ageClassifier.train_classifier (train_data)
genderClassifier.train_classifier (train_data)


def classify(location):
	return User (None, genderClassifier.classify (location).result, ageClassifier.classify (location).result)