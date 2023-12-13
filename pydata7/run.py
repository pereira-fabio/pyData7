from pydata7.scripts.repo_downloader import foo
from pydata7.database_manager.connect_to_db import get_db

if __name__ == "__main__":
    # establishing the mongo connection
    get_db()

    # download the diffs and other content
    foo()
