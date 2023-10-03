import logging
import pymongo
import os
import json

# Get the current directory
current_dir = os.path.dirname(os.path.abspath(__file__))

# Relative path to the data file
data_file = "../data_generator/data.json"

# Absolute path to the data file
full_path = os.path.normpath(os.path.join(current_dir, data_file))

host = "localhost"
port = 27017  # The default MongoDB port

username = "root"
password = "example"
database_name = "data7"

def import_data():
    # Connect to MongoDB
    logging.info("Connecting to MongoDB")

    connection_string = f"mongodb://{username}:{password}@{host}:{port}/{database_name}"
    myclient = pymongo.MongoClient(connection_string)
    db = myclient[database_name]
    #collection = db.your_collection_name
    #dblist = myclient.list_database_names()
    #if "data7" in dblist:
        #print("The database exists.")
    print("connected")
    logging.info("Connected to MongoDB")
    # Import data
    print("Importing data")
    logging.info("Importing data")
    with open(full_path) as f:
        file_data = json.load(f)
        #print(file_data)

    collection = db['data7']
    print("inserting")
    collection.insert_many(file_data)
    logging.info("Data imported")

if __name__ == "__main__":
    import_data()

