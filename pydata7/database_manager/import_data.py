from pydata7.database_manager.connect_to_db import get_db, get_client, connection, close_connection
import os

path_to_data = "pydata7/data/json_files/"


# Imports data into the database by going through the data folder
# Since any data might be needed in the future, it makes sense to import all the data
def import_data():
    # Establish mongo connection
    connection()
    # Dropping collections if they exist (might remove it, since we want to update the data and not drop it)
    if len(get_db().list_collection_names()) != 0:
        print("The database is not empty")
        get_client().drop_database("pydata7")
        print("The database was dropped")
    # Checking if the database is empty (the condition might change as well)
    if len(get_db().list_collection_names()) == 0:
        print("The database is empty")
        # Creating collections
        for filename in os.listdir(path_to_data):
            if filename.endswith(".json"):
                # Splits the name of the file and gets the first two parts
                parts = filename.split("_")[0:2]
                # Joins the first two parts and creates a collection name
                collection_name = parts[0] + "_" + parts[1]
                # Creates a collection
                collection = get_db()["".join(collection_name)]
                insert_data(path_to_data + filename, collection)
                print(collection_name, "was inserted into the database")


# Inserting data into the database
def insert_data(path_to_filedata, collection):
    with open(path_to_filedata, "r") as f:
        collection.insert_many(eval(f.read()))


if __name__ == "__main__":
    import_data()
