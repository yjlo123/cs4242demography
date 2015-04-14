import tweets
import train

M = "MALE"
F = "FEMALE"

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

test_trainer = train.Trainer ()
test_trainer.load_database("online.csv", -1)

# generate test set (fold 1-10)
test_set = test_trainer.get_all_test_id()

male = [0,0,0]
female = [0,0,0]
age_match = 0
count = 0
for uid in test_set:
	predicted = tweets.classify_user(gender_classifier, age_classifier, uid)
	p_gender = predicted[0]
	a_gender = test_trainer.get_gender_by_id(uid)
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
	a_age = test_trainer.get_age_by_id(uid)
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
	if a[1]+a[2] != 0:
		f1 = (2.0*a[1]*a[2])/(a[1]+a[2])
	print "["+name+"] "+str(precision)+"/"+str(recall)+"/"+str(f1)

print_result("MALE", male)
print_result("FEMALE", female)
accuracy = (male[0]+female[0])/float(len(test_set))
print "[Gender Accuracy]"+str(accuracy)
print "[Age Accuracy]"+str(age_match/float(len(test_set)))
#classify_user("834c49eb87d78c8d56e5a7c3b76b2391")

