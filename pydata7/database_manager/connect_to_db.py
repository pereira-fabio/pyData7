import pymongo.errors
from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()

# Connecting to the database
hostname = os.getenv("HOST_NAME")
port = os.getenv("PORT")
user = os.getenv("USER_MONGO")
password = os.getenv("PASSWORD_MONGO")
client = MongoClient(hostname, port, username=user, password=password)
# client = MongoClient("mongodb://localhost:27017/")
mydb = client["pydata7"]  # database name


def connection():
    if client.server_info():
        print("Connection established:", client.address)
    else:
        print("Connection not established.")


def get_db():
    return mydb


def get_client():
    return client


def close_connection():
    client.close()
    try:
        client.server_info()
    except pymongo.errors.InvalidOperation:
        print("Connection closed.")
