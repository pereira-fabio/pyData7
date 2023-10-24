from pymongo import MongoClient

# I can only connect to a database which is not running on docker container
# Connecting to the database
myclient = MongoClient("mongodb://localhost:27017/")
mydb = myclient["pydata7"]  # database

# Dropping collections if they exist
#mydb.drop_collection("filtered")
#mydb.drop_collection("unfiltered")

# Creating collections
filtered_collection = mydb["filtered"]
unfiltered_collection = mydb["unfiltered"]
commits_collection = mydb["commits"]
org_proj_collection = mydb["org_proj"]

# Path to the data (will change)
path_to_filtered = "../data/filtered_data_2023-10-24_17-32-15.json"
path_to_unfiltered = "../data/raw_data_2023-10-24_17-31-20.json"
path_to_valid = "../data/contains_commit_2023-10-24_17-59-03.json"
path_to_org_proj = "../data/org_proj_2023-10-24_17-59-03.json"

# the data is inserted only if the collection is empty (only for testing purposes)
# Inserting data into the database
if filtered_collection.count_documents({}) == 0:
    with open(path_to_filtered, "r") as f:
        filtered_collection.insert_many(eval(f.read()))

if unfiltered_collection.count_documents({}) == 0:
    with open(path_to_unfiltered, "r") as f:
        unfiltered_collection.insert_many(eval(f.read()))

if commits_collection.count_documents({}) == 0:
    with open(path_to_valid, "r") as f:
        commits_collection.insert_many(eval(f.read()))

if org_proj_collection.count_documents({}) == 0:
    with open(path_to_org_proj, "r") as f:
        org_proj_collection.insert_many(eval(f.read()))

print(filtered_collection.find_one())