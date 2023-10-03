import json
import re
import os

# Path to the filtered data
save_path = "../filtered_data/"

# Path to the regex patterns
path_to_platform = "../regex/platform.json"

# Will change. This is just for testing.
path_to_json = "../unfiltered_data/data_2023-10-03_13-52-43.json"

# Load the regex patterns from platform.json
with open(path_to_platform, "r") as regex_file:
    regex_data = json.load(regex_file)

# Load data from the data_generator
with open(path_to_json, "r") as data_file:
    data = json.load(data_file)

# A Dictionary to store the filtered data
filtered_data = []


# This function will return a list of dictionaries with the CVE ID (might contain duplicates)
def get_unique_cve_id(path_to_json):
    with open(path_to_json, "r+") as json_file:
        data = json.load(json_file)
        cveid_list = []
        for item in data:
            cveid_list.append(item['cve_id'])
        return list(set(cveid_list))


def data_filtering():
    # Iterate through the regex patterns
    for regex in regex_data:
        # A list to store the complied regex
        list_regex = []
        # Iterate through the regex patterns and compile them
        for regex in regex["regexps"]:
            # Compile the regex from platform.json
            complied_regex = re.compile(regex["regexp"])
            list_regex.append(complied_regex)
        # Iterate through the data and check if the url matches the regex
        for item in data:
            # Iterate through the list of complied regex
            for regex in list_regex:
                # Check if the url matches the regex
                if regex.search(item["url"]):
                    filtered_data.append(item)

    file_name = "filtered_data.json"
    file_path = os.path.join(save_path, file_name)
    # Write the filtered data to a json file
    with open(file_path, "w") as filtered_file:
        json.dump(filtered_data, filtered_file)
    return filtered_data


data_filtering()
