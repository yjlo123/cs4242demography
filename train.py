import csv
import pprint

class Trainer:
	def __init__ (self):
		self.__train_data = {}

	# Read the database file into the train_data field as a list of Record tuple
	def load_database (self, filename, train_size):
		# Load the train database into memory
		pp = pprint.PrettyPrinter(indent=4)

		f_input = open (filename, 'rU')
		reader = csv.reader (f_input)
		next (reader)


		record_read = 0
		for row in reader:
			#print row
			self.__train_data[row[0]]=(row[1], row[2])
			record_read += 1
			if train_size >= 0 and record_read >= train_size:
				break
		#pp.pprint(self.__train_data)
		#print self.__train_data["fd36e6c9c129dbdc501d7e4d4190fc9e"]
	def is_in_train(self, id):
		return id in self.__train_data

	def get_gender_by_id(self, id):
		return self.__train_data[id][0]

	def get_age_by_id(self, id):
		return self.__train_data[id][1]

	def get_fold_test_set(self, fold):
		train_set = []
		test_set = []
		total_size = len(self.__train_data)
		lower_bound = (fold-1)*(total_size/10)
		upper_bound = (fold)*(total_size/10)
		curr = 0
		for key in self.__train_data:
			if curr >= lower_bound and curr < upper_bound:
				test_set.append(key)
			else:
				train_set.append(key)
			curr += 1
		return (train_set, test_set)
	def get_all_test_id(self):
		test_set = []
		for key in self.__train_data:
			test_set.append(key)
		return test_set