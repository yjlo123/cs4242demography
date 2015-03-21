from haversine_distance import HaversineDistance
from params import *
from namedtuple import *

class CheckInClassifier:
	def __init__ (self, feature = None, radius = None):
		self.__isTrained = False
		self.__isFeatureSet = False
		self.__data = []
		self.__feature_name = None
		self.__classify_type = []
		self.__classify_count = []
		self.__radius = CLASSIFY_RADIUS

		if feature != None:
			self.set_feature (feature)
		if radius != None:
			self.__radius = radius

	def __train_entry__ (self, entry):
		# Do no process incomplete entries
		if entry.user == None or entry.location == None:
			return

		# Assert that the feature exists
		user = entry.user._asdict ()
		assert self.__feature_name in user.keys ()

		# Append the entry into the data list
		self.__data.append (entry)

		# Extract feature out from the entry
		feature = user[self.__feature_name]

		# Add feature to the list of feature collected
		if feature not in self.__classify_type:
			self.__classify_type.append (feature)
			self.__classify_count.append (1)
		else:
			index = self.__classify_type.index (feature)
			self.__classify_count[index] += 1

	# Select with feature to extract
	# Params:
	#	feature: the name of the feature to, either "gender" or "ageGroup"
	#			 the feature name should exist in User tuple
	def set_feature (self, feature):
		if feature == "gender" or feature == "ageGroup":
			self.__isFeatureSet = True
			self.__feature_name = feature

	# Train the classifier with the train data set
	# Params:
	#	data: a list of CheckInFeature tuple
	def train_classifier (self, data):
		if self.__isFeatureSet:
			self.__isTrained = True
			for entry in data:
				self.__train_entry__ (entry)
		else:
			print "Feature has not yet set. Please set feature via set_feature method"


	# Update the classifier with more data to train
	# Params:
	#	data: a list of CheckInFeature tuple
	def append_train_data (self, data):
		if self.__isFeatureSet:
			for entry in data:
				train_entry(entry)
		else:
			print "Feature has not yet set. Please set feature via set_feature method"

	# Whether the classifier is read to classifer location
	# Return:
	#	a boolean value to state whether the classifier is ready
	def is_trained (self):
		return self.__isTrained and self.__isFeatureSet

	def __get_nearest_location__ (self, location, radius):
		nearest = []
		for entry in self.__data:
			if HaversineDistance (	entry.location.latitude, \
									entry.location.longidute, \
									location.latitude, \
									location.longidute) < radius:
				nearest.append (entry)

		return nearest

	# Try to classify an user based on his location
	# Params:
	#	location: a Location tuple providing information of the location
	# Return:
	#	a ClassifyResult tuple providing information of the user, as well as how confident
	#	is the result
	#	return None if the classifer is not trained yet
	def classify (self, location):
		if self.is_trained:
			# Get all the nearest trained checkins from database			
			nearest_entries = self.__get_nearest_location__ (location, self.__radius)

			# Calculate the total entries, total nearest entries, and the frequence of the entries based on features
			total_entry = len (self.__data)
			total_nearest = len (nearest_entries)
			classify_nearest = [0] * len (self.__classify_type)

			# If cannot retrieve any near hit, then cannot classify
			if total_nearest == 0:
				result = ClassifyResult (None, 0)
				return result

			for entry in nearest_entries:
				feature = entry.user._asdict()[self.__feature_name]
				index = self.__classify_type.index (feature)
				classify_nearest[index] += 1

			# For each feature type, calculate the probability based on Naive Bayes
			probablity = [0] * len (self.__classify_type)
			for index in range (0, len (self.__classify_type)):
				prio_prob = float (self.__classify_count[index]) / total_entry
				proximate_prob = float (classify_nearest[index]) / total_nearest
				probablity[index] = prio_prob * proximate_prob

			# Get the highest probability index
			# Also sum up the total probablity
			highest_index = 0
			prob_sum = 0
			for index in range (0, len (probablity)):
				prob_sum += probablity[index]
				if probablity[index] > probablity[highest_index]:
					highest_index = index

			# Report the result
			classify_type = self.__classify_type[highest_index]
			classify_confident = probablity[highest_index] / prob_sum
			result = ClassifyResult (classify_type, classify_confident)
			return result
		else:
			print "Classifier is not trained yet."


		