import json
import re
from pydata7.links_processing.link_filter import data_filtering
from pydata7.scripts.json_file_generation import json_file_generation

# Path to the data from the data_generator
# path_to_json = data_filtering()

# For testing purposes
path_to_json = "../data/json_files/filtered_data_2023-11-14_16-55-56.json"

# A list to store the data that contains a commit
contains_commit = []
contains_issues = []

with open(path_to_json, "r") as file:
    data = json.load(file)

test = []


def has_commit():
    for item in data:
        if "commit" in item["url"]:
            # Get the organization and project name from the url
            # For GitHub links only
            parts = item["url"].split("/")
            repository = "https://" + parts[2] + "/" + parts[3] + "/" + parts[4]
            commit_sha = parts[6]
            if is_alphanumeric(commit_sha):
                # Add the organization and project name to the dictionary
                item["repository"] = repository
                item["commit_sha"] = commit_sha
                # Add the dictionary to the list
                contains_commit.append(item)
                print(len(contains_commit))
            else:
                part_sha = commit_sha.split("#diff-")
                # Add the organization and project name to the dictionary
                item["repository"] = repository
                item["commit_sha"] = part_sha[0]
                # Add the dictionary to the list
                contains_commit.append(item)
                print(len(contains_commit))

        elif "issues" in item["url"]:
            # Add the dictionary to the list
            contains_issues.append(item)
    # This is generated if needed later
    json_file_generation(contains_issues, "contains_issues")
    # This is the main function that will be used
    return json_file_generation(contains_commit, "contains_commit")


def is_alphanumeric(commit_sha):
    regex_pattern = r"^[a-zA-Z0-9]+$"
    return re.match(regex_pattern, commit_sha) is not None


def sorted_data():
    with open(has_commit(), "r") as f:
        d = json.load(f)

    sorted_data_list = sorted(d, key=lambda k: k['repository'])
    return json_file_generation(sorted_data_list, "sorted_commit")


if __name__ == "__main__":
    sorted_data()
