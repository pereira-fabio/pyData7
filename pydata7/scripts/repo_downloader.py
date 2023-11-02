# The only way to run this in windows is to use the WSL
# cd /mnt/c/Users/perei/Desktop/Project/pydata7/scripts
# python3 repo_downloader.py
import os
from git import Repo
from dotenv import load_dotenv

print(load_dotenv())
path_to_data = os.getenv("PATH_TO_DATA")

print(path_to_data)


# Clones the repository
def clone_repo():
    Repo.clone_from("https://github.com/pereira-fabio/pyData7/", "../data/repos")


if __name__ == "__main__":
    clone_repo()
