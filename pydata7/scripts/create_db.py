from pymongo import MongoClient
import os

# I can only connect to a database which is not running on docker container
# Connecting to the database
myclient = MongoClient("mongodb://localhost:27017/")
mydb = myclient["pydata7"]  # database name

path_to_data = "../data/json_files/"


# Imports data into the database by going through the data folder
# Since any data might be needed in the future, it makes sense to import all the data
def import_data():
    # Dropping collections if they exist (might remove it, since we want to update the data and not drop it)
    if len(mydb.list_collection_names()) != 0:
        print("The database is not empty")
        myclient.drop_database("pydata7")
        print("The database was dropped")
    # Checking if the database is empty (the condition might change as well)
    if len(mydb.list_collection_names()) == 0:
        print("The database is empty")
        # Creating collections
        for filename in os.listdir(path_to_data):
            if filename.endswith(".json"):
                # Splits the name of the file and gets the first two parts
                parts = filename.split("_")[0:2]
                # Joins the first two parts and creates a collection name
                collection_name = parts[0] + "_" + parts[1]
                # Creates a collection
                collection = mydb["".join(collection_name)]
                insert_data(path_to_data + filename, collection)
                print(collection_name, "was inserted into the database")


# Inserting data into the database
def insert_data(path_to_filedata, collection):
    with open(path_to_filedata, "r") as f:
        collection.insert_many(eval(f.read()))


if __name__ == "__main__":
    import_data()
