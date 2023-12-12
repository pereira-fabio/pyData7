from pymongo import MongoClient

# I can only connect to a database which is not running on docker container
# Connecting to the database
hostname = "localhost"
port = 27017
user = "root"
password = "example"
client = MongoClient(hostname, port, username=user, password=password)
# client = MongoClient("mongodb://localhost:27017/")
mydb = client["pydata7"]  # database name


def get_db():
    return mydb


def get_client():
    return client
