import tweets
import train

classifiers = tweets.train()
# i pass you the t_classifiers

gender_classifier = classifiers[0]
age_classifier = classifiers[1]
'''
t = "tweet text"
t = tweets.tweet_to_keywords(t)
result = gender_classifier.classify(t)
print result
'''
trainer = train.Trainer ()
trainer.load_database("train.csv", -1)

# generate test set (fold 1-10)
eval_set = trainer.get_fold_test_set(2)
test_set = eval_set[1]

for uid in test_set:
	print tweets.classify_user(gender_classifier, age_classifier, uid)
	print trainer.get_gender_by_id(uid)

#classify_user("834c49eb87d78c8d56e5a7c3b76b2391")
