# The only way to run this in windows is to use the WSL
# cd /mnt/c/Users/perei/Desktop/Project/pydata7/scripts
# python3 repo_downloader.py
import os
import git
import json
import datetime
import shutil
# from pydata7.links_processing.valid_link import sorted_data
from json_file_generation import json_file_generation

# path_to_json = sorted_data()
# path_to_json = "../data/json_files/test_2023-11-11_15-27-47.json"
path_to_json = "../data/json_files/sorted_commit_2023-11-14_16-55-57.json"

# A list that stores everything of the commit information
commit_content = []

with open(path_to_json, "r") as file:
    data = json.load(file)


# Do not know how to call the function
def foo():
    print(range(len(data) - 1))
    for i in range(10 - 1):
        print(i)
        current_repo_url = data[i]["repository"]
        next_repo_url = data[i + 1]["repository"]

        commit_sha = data[i]["commit_sha"]

        parts = data[i]["url"].split("/")
        repository = parts[3] + "/" + parts[4]
        path = "../data/repos/"
        path_repo = path + repository

        if current_repo_url == next_repo_url:
            print("Same repository")

            data[i]["commit_info"] = commit_handler(path_repo, current_repo_url, commit_sha)
            commit_content.append(data[i])
            print("Same repository")
        else:
            print("Different repository")

            data[i]["commit_info"] = commit_handler(path_repo, current_repo_url, commit_sha)
            commit_content.append(data[i])
            shutil.rmtree(path)
            print("Different repository")

    # for item in data:
    #     repo_url = item["repository"]
    #     commit_sha = item["commit_sha"]
    #
    #     parts = item["url"].split("/")
    #     repository = parts[3] + "/" + parts[4]
    #     path = "../data/repos/"
    #     # Sets the path to the repository using the organization and project name
    #     path_repo = path + repository
    #
    #     # Clones the repository if it does not exist
    #     if os.path.exists(path_repo):
    #         repo = git.Repo(path_repo)
    #         print("Repository already exists")
    #     else:
    #         repo = git.Repo.clone_from(repo_url, path_repo)
    #     print("Repository was cloned")
    #
    #     # Get the commit before the specified commit
    #     commit_sha2 = commit_sha + "~1"
    #
    #     # Get the commit objects for the specified SHAs
    #     commit1 = repo.commit(commit_sha)
    #     commit2 = repo.commit(commit_sha2)
    #
    #     # Get the commit information and add it to the list
    #     commit_info = {
    #         # str() is used to convert the object to string -> otherwise it will cause an error with JSON
    #         "commit_author": str(commit1.author),
    #         # Convert the timestamp to a readable date format
    #         "commit_date": str(datetime.datetime.fromtimestamp(commit1.authored_date)),
    #         "commit_message": str(commit1.message),
    #         "commit_diff": repo.git.diff(commit1, commit2)
    #     }
    #     commit_info_list.append(commit_info)
    #
    #     # Add the commit information to the dictionary
    #     item["commit_info"] = commit_info_list
    #     # Add the dictionary to the list
    #     commit_content.append(item)

    return json_file_generation(commit_content, "commit_info")


def commit_handler(path_repo, repo_url, commit_sha):
    # A list to store the commit information
    commit_info_list = []
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

    author = str(commit1.author)
    message = commit1.message.encode('utf-8', 'ignore')
    message = message.decode('utf-8')
    if isinstance(message, (bytes, bytearray, memoryview)):
        print("Message: It is a byte string")

    diff = repo.git.diff(commit1, commit2).encode('utf-8', 'ignore')
    diff = diff.decode('utf-8')
    if isinstance(diff, (bytes, bytearray, memoryview)):
        print("Diff: It is a byte string")

    # Get the commit information and add it to the list
    commit_info = {
        # str() is used to convert the object to string -> otherwise it will cause an error with JSON
        "commit_author": author,
        # Convert the timestamp to a readable date format
        "commit_date": str(datetime.datetime.fromtimestamp(commit1.authored_date)),
        "commit_message": message,
        "commit_diff": diff
    }
    commit_info_list.append(commit_info)
    return commit_info_list


if __name__ == "__main__":
    foo()
