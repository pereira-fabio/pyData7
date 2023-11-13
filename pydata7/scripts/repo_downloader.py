# The only way to run this in windows is to use the WSL
# cd /mnt/c/Users/perei/Desktop/Project/pydata7/scripts
# python3 repo_downloader.py
import os
import git
import json
import datetime
from git import Repo
#from pydata7.links_analysis.valid_link import has_commit
from json_file_generation import json_file_generation

# path_to_json = has_commit()
path_to_json = "../data/json_files/test.json"

# A list to store the commit information
commit_info_list = []
# A list that stores everything of the commit information
commit_content = []

with open(path_to_json, "r") as file:
    data = json.load(file)


# Do not know how to call the function
def foo():
    for item in data:
        repo_url = item["repository"]
        commit_sha = item["commit_sha"]

        parts = item["url"].split("/")
        repository = parts[3] + "/" + parts[4]
        path = "../data/repos/"
        # Sets the path to the repository using the organization and project name
        path_repo = path + repository

        # Clones the repository if it does not exist
        if os.path.exists(path_repo):
            repo = git.Repo(path_repo)
            print("Repository already exists")
        else:
            repo = git.Repo.clone_from(repo_url, path_repo)
        print("Repository was cloned")

        # Get the commit before the specified commit
        commit_sha2 = commit_sha + "~1"

        # Get the commit objects for the specified SHAs
        commit1 = repo.commit(commit_sha)
        commit2 = repo.commit(commit_sha2)

        # Get the commit information and add it to the list
        commit_info = {
            # str() is used to convert the object to string -> otherwise it will cause an error with JSON
            "commit_author": str(commit1.author),
            # Convert the timestamp to a readable date format
            "commit_date": str(datetime.datetime.fromtimestamp(commit1.authored_date)),
            "commit_message": str(commit1.message),
            "commit_diff": repo.git.diff(commit1, commit2)
        }
        commit_info_list.append(commit_info)

        # Add the commit information to the dictionary
        item["commit_info"] = commit_info_list
        # Add the dictionary to the list
        commit_content.append(item)

    json_file_generation(commit_content, "commit_info")


if __name__ == "__main__":
    foo()
