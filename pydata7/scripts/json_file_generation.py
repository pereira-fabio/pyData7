import datetime
import json
import os

save_path = "../data/json_files/"


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
