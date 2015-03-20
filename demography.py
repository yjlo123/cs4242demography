import pymongo

client = pymongo.MongoClient("localhost", 27017)
db = client.cs4242

print db.users.find()[0]["description"]