# The only way to run this in windows is to use the WSL
# cd /mnt/c/Users/perei/Desktop/Project/pydata7/scripts
# python3 repo_downloader.py
import os
os.environ["GIT_PYTHON_REFRESH"] = "quiet"
import git
import json
import datetime
import shutil
# from pydata7.links_processing.valid_link import sorted_data
from pydata7.scripts.json_file_generation import json_file_generation
from pydata7.database_manager.import_data import import_data

# path_to_json = sorted_data()
# path_to_json = "../data/json_files/test_2023-11-11_15-27-47.json"
path_to_json = "pydata7/data/json_files/test_2023-11-11_15-27-47.json"

# A list that stores everything of the commit information
commit_content = []

with open(path_to_json, "r") as file:
    data = json.load(file)


# Do not know how to call the function
def foo():
    print(range(len(data) - 1))
    for i in range(len(data) - 1):
        print(i)
        # Get the current and next repository url
        current_repo_url = data[i]["repository"]
        next_repo_url = data[i + 1]["repository"]

        # Get the commit sha
        commit_sha = data[i]["commit_sha"]

        # Get the organization and project name from the url
        # To create a path to the repository while cloning
        parts = data[i]["url"].split("/")
        repository = parts[3] + "/" + parts[4]
        path = "pydata7/data/repos/"
        path_repo = path + repository

        # Check if the current and next repository url are the same
        # If they are the same, then the repository is already cloned
        if current_repo_url == next_repo_url:
            print("Same repository")
            # Get the commit information
            data[i]["commit_info"] = commit_handler(path_repo, current_repo_url, commit_sha)
            commit_content.append(data[i])
        else:
            print("Different repository")
            # Get the commit information
            data[i]["commit_info"] = commit_handler(path_repo, current_repo_url, commit_sha)
            commit_content.append(data[i])
            # Delete the repository if it is not the same
            shutil.rmtree(path+parts[3])

    return json_file_generation(commit_content, "commit_info")


def commit_handler(path_repo, repo_url, commit_sha):
    # A list to store the commit information
    commit_info_list = []

    # Clones the repository if it does not exist
    if os.path.exists(path_repo):
        repo = git.Repo(path_repo)
        print("Repository already exists no need to clone")
    else:
        os.makedirs(path_repo, exist_ok=True)
        print(path_repo, "was created")
        repo = git.Repo.clone_from(repo_url, path_repo)
    print("Repository was cloned")

    # Get the commit before the specified commit
    commit_sha2 = commit_sha + "~1"

    # Get the commit objects for the specified SHAs
    commit1 = repo.commit(commit_sha)
    commit2 = repo.commit(commit_sha2)

    # str() is used to convert the object to string -> otherwise it will cause an error with JSON
    author = str(commit1.author)
    # Convert the timestamp to a readable date format
    date = str(datetime.datetime.fromtimestamp(commit1.authored_date))

    # Convert the message to byte string and then to string
    message = commit1.message.encode('utf-8', 'ignore')
    message = message.decode('utf-8')
    if isinstance(message, (bytes, bytearray, memoryview)):
        print("Message: It is a byte string")

    # Convert the message to byte string and then to string
    diff = repo.git.diff(commit1, commit2).encode('utf-8', 'ignore')
    diff = diff.decode('utf-8')
    if isinstance(diff, (bytes, bytearray, memoryview)):
        print("Diff: It is a byte string")

    # Get the commit information and add it to the list
    commit_info = {
        "commit_author": author,
        "commit_date": date,
        "commit_message": message,
        "commit_diff": diff
    }
    commit_info_list.append(commit_info)
    return commit_info_list


if __name__ == "__main__":
    foo()
    import_data()
