# The only way to run this in windows is to use the WSL
# cd /mnt/c/Users/perei/Desktop/Project/pydata7/scripts
# python3 repo_downloader.py
import os
import git
from git import Repo
from dotenv import load_dotenv

print(load_dotenv())
path_to_data = os.getenv("PATH_TO_DATA")
repo_url = "https://github.com/pereira-fabio/pyData7"
commit_sha = "1705798b994f3fdda1754876a14a42121c183c37"
# def retrieving_file_from_specific_commit(repo: Repo, commit: str, path: str) -> str:
#     """
#     Function to return a file from a specific commit
#
#     Parameters:
#         repo (Repo): repository object
#         commit (str): commit string
#         path (str): path of the file to load
#
#     Returns:
#         the content of the file (str)
#     """
#     return repo.git.show("{}:{}".format(commit, path))
#

# Clones the repository
path_repo= "../data/repos"

if os.path.exists(path_repo):
    repo = git.Repo(path_repo)
else:
    repo = git.Repo.clone_from(repo_url, path_repo)

commit = repo.commit(commit_sha)

destination = "../data/commit"
os.makedirs(destination, exist_ok=True)

for item in commit.tree.traverse():
    if item.type == "blob":
        path = os.path.join(path_repo, item.path)
        destination_path = os.path.join(destination, item.path)

        os.makedirs(os.path.dirname(destination_path), exist_ok=True)
        with open(destination_path, "wb") as f:
            with open(path, "rb") as original:
                f.write(original.read())

print(f"Commit content from {commit_sha} is saved in {destination}")

# Define the commit SHAs for comparison
commit_sha1 = "1705798b994f3fdda1754876a14a42121c183c37"
commit_sha2 = commit_sha1 + "~1"

# Get the commit objects for the specified SHAs
commit1 = repo.commit(commit_sha1)
commit2 = repo.commit(commit_sha2)

# Display the diff between the two commits
print(repo.git.diff(commit1, commit2))
