import asyncio
import aiohttp
import requests
import json
import os
import datetime
from pydata7.links_analysis.link_filter import data_filtering

# Path to the filtered data
save_path = "../data/"

# Path to the data from the data_generator
path_to_json = data_filtering()

# A list to store the data that contains a commit
contains_commit = []

with open(path_to_json, "r") as f:
    data = json.load(f)


def has_commit():
    for item in data:
        if "commit" in item["url"]:
            # Get the organization and project name from the url
            organization_project = item["url"].split("/")[3:5]
            # Add the organization and project name to the dictionary
            item["organization_project"] = organization_project
            # Add the dictionary to the list
            contains_commit.append(item)
    return json_file_generation(contains_commit, "contains_commit")

#TODO check if the links is already in the database
def is_valid():
    valid_links = []
    with open(has_commit(), "r") as f:
        valid_commit_links = json.load(f)

    for item in valid_commit_links:
        parts = item["url"].split("/")
        repository = "https://" + parts[2] + "/" + parts[3] + "/" + parts[4]
        try:
            response = requests.head(repository)
            if response.status_code == 200:
                valid_links.append(item)
        except requests.exceptions.RequestException as err:
            raise SystemExit(err)
    return json_file_generation(valid_links, "valid_links")


def json_file_generation(array, name):
    # Gets the current date and time as a string. Year - Month - Day _ Hour - Minute - Second
    current_time = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

    # Saves the data into a json file with the current date and time
    file_name = f"{name}_{current_time}.json"

    # Creates the path to save the json file
    file_path = os.path.join(save_path, file_name)

    # Writes the data into a json file
    with open(file_path, "w") as json_file:
        json.dump(array, json_file)

    # returns the path to the json file, so it can be used in the next function
    return file_path


if __name__ == "__main__":
    is_valid()
