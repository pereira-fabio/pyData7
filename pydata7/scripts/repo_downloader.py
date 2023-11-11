# The only way to run this in windows is to use the WSL
# cd /mnt/c/Users/perei/Desktop/Project/pydata7/scripts
# python3 repo_downloader.py
import os
import git
from git import Repo
from dotenv import load_dotenv
import datetime

print(load_dotenv())
path_to_data = os.getenv("PATH_TO_DATA")
repo_url = "https://github.com/pereira-fabio/pyData7"
#repo_url = "https://github.com/KDE/kde1-kdebase"
commit_sha = "1705798b994f3fdda1754876a14a42121c183c37"
#commit_sha = "04906bd5de2f220bf100b605dad37b4a1d9a91a6"


# Clones the repository
path_repo = "../data/repos/"
path_repo_url = path_repo + repo_url

if os.path.exists(path_repo_url):
    repo = git.Repo(path_repo_url)
else:
    repo = git.Repo.clone_from(repo_url, path_repo_url)

commit = repo.commit(commit_sha)

# destination = "../data/commit"
# os.makedirs(destination, exist_ok=True)
#
# for item in commit.tree.traverse():
#     if item.type == "blob":
#         path = os.path.join(path_repo, item.path)
#         destination_path = os.path.join(destination, item.path)
#
#         os.makedirs(os.path.dirname(destination_path), exist_ok=True)
#         with open(destination_path, "wb") as f:
#             with open(path, "rb") as original:
#                 f.write(original.read())

# print(f"Commit content from {commit_sha} is saved in {destination}")

# Define the commit SHAs for comparison
commit_sha1 = commit_sha + "~1"

# Get the commit objects for the specified SHAs
commit1 = repo.commit(commit_sha)
commit2 = repo.commit(commit_sha1)

# Display the diff between the two commits
print(repo.git.diff(commit1, commit2))

print("author: ", commit1.author)
print("date: ", datetime.datetime.fromtimestamp(commit1.authored_date))
print("message: ", commit1.message)
