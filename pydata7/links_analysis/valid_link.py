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
path_to_json = data_filtering()  # "../data/filtered_data_2023-10-04_15-09-07.json"

# A Dictionary to store filtered data which only contains the 200 status code
valid_data = []

with open(path_to_json, "r") as f:
    data = json.load(f)


async def valid_link(item, session):
    url = item.get("url")
    # Checks if the url is not empty
    if url:
        # In case of a timeout or a connection error, the program will exit
        try:
            async with session.head(url) as response:
                # Checks if the response is 200 as it is the only valid response
                if response.status == 200:
                    # Adds the item to the valid_data list
                    valid_data.append(item)
                    print(len(valid_data), "links were validated")
                else:
                    # print how many are not valid
                    print(f"{response.status} is not valid")
        except aiohttp.ClientError as err:
            print(f"An error occurred while checking the URL {url}: {err}")
    else:
        print("No URL found")


async def process_data():
    async with aiohttp.ClientSession() as session:
        tasks = []
        for item in data:
            task = valid_link(item, session)
            tasks.append(task)
        await asyncio.gather(*tasks)
        print(len(valid_data), "links were validated")
        json_file_generation()


def json_file_generation():
    # Gets the current date and time as a string. Year - Month - Day _ Hour - Minute - Second
    current_time = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

    # Saves the data into a json file with the current date and time
    file_name = f"valid_data_{current_time}.json"

    # Creates the path to save the json file
    file_path = os.path.join(save_path, file_name)

    # Writes the data into a json file
    with open(file_path, "w") as json_file:
        json.dump(valid_data, json_file)

    # returns the path to the json file, so it can be used in the next function
    return file_path


if __name__ == "__main__":
    asyncio.run(process_data())
