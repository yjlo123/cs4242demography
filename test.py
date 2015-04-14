import tweets
import train
import checkins
import description

M = "MALE"
F = "FEMALE"

print "initializing..."
classifiers = tweets.train()
gender_classifier = classifiers[0]
age_classifier = classifiers[1]
description_classifier = description.train()


def fusion_result(uid):
	checkin_result = checkins.predict_by_checkin(uid)
	tweet_result = tweets.classify_user(gender_classifier, age_classifier, uid)
	description_text = description.uid_to_description(uid)
	description_result = description.classify(description_classifier, description_text)
	return tweet_result

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

#Evaluation
male = [0,0,0]
female = [0,0,0]
age_match = 0
print "Calculating results..."
count = 0
for uid in test_set:
	predicted = fusion_result(uid)
	p_gender = predicted[0]
	a_gender = trainer.get_gender_by_id(uid)
	if p_gender == M:
		male[1]+=1
	else:
		female[1]+=1
	if a_gender == M:
		male[2]+=1
	else:
		female[2]+=1
	if p_gender == a_gender:
		if p_gender == M:
			male[0]+=1
		else:
			female[0]+=1
	p_age = predicted[1]
	a_age = trainer.get_age_by_id(uid)
	if p_age == a_age:
		age_match+=1
	count+=1
	print str(count)+"/"+str(len(test_set))

def print_result(name, a):
	precision = recall = f1 = 0
	if a[1] != 0.0:
		precision = a[0]/float(a[1])
	if a[2] != 0.0:
		recall = a[0]/float(a[2])
	if precision+recall != 0:
		f1 = (2.0*precision*recall)/(precision+recall)
	print "["+name+"] "+str(precision)+"/"+str(recall)+"/"+str(f1)

print_result("MALE", male)
print_result("FEMALE", female)
accuracy = (male[0]+female[0])/float(len(test_set))
print "[Gender Accuracy]"+str(accuracy)
print "[Age Accuracy]"+str(age_match/float(len(test_set)))
#classify_user("834c49eb87d78c8d56e5a7c3b76b2391")
