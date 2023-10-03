import json
import re

path_to_platform = "../regex/platform.json"

# Will change. This is just for testing.
path_to_json = "../data_generator/data_2023-10-03_13-52-43.json"

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
    for regex in regex_data:
        list_regex = []
        for regex in regex["regexps"]:
            complied_regex = re.compile(regex["regexp"])
            list_regex.append(complied_regex)
        for item in data:
            for regex in list_regex:
                if regex.search(item["url"]):
                    filtered_data.append(item)
    with open("filtered_data.json", "w") as filtered_file:
        json.dump(filtered_data, filtered_file)
    return filtered_data

data_filtering()
