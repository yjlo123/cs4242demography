### Package parameters
MONGO_HOST = "localhost"		### Mongodb host
MONGO_PORT = 27017				### Mongodb port
TEST_FOLD = 0					### the fold id to test, will not load this
								### fold when trainning
FOLD_COUNT = 10					### number of fold to split the database
USER_DATA_FILE = "train.csv"	### user information to train

### Train parameters
CLASSIFY_RADIUS = 400			### Default result: How far should the
								### Naive Bayes look for proximate checkins