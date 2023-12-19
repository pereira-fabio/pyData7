from pydata7.scripts.repo_downloader import foo
# from pydata7.database_manager.connect_to_db import get_db, get_client, connection, close_connection
from pydata7.fastapi.api import run_uvicorn

if __name__ == "__main__":
    # download the diffs and other content
    print("Getting diff:")
    foo()

    # start FastAPI server
    print("Running API server:")
    run_uvicorn()
