from pymongo import MongoClient
# I can only connect to a database which is not running on docker container
myclient = MongoClient("mongodb://localhost:27017/")
mydb = myclient.pydata7  # database

print(myclient.list_database_names())