from pydata7.database_manager.connect_to_db import get_db
from fastapi import FastAPI, HTTPException, Depends

app = FastAPI()


def get_database():
    db = get_db()
    return db


def get_collection(collection_name: str, db=Depends(get_database)):
    return db[collection_name]


# Returns the collection containing the diff
def get_diff_collection(db=Depends(get_database)):
    return db["commit_diff"]


# Base URL
@app.get("/")
def read_root():
    return {"message": "Hello,PyData7"}


# Lists every collection in the client pydata7
@app.get("/collections")
def get_collections(db=Depends(get_database)):
    names_list = []
    collections_list = db.list_collection_names()
    print("Available Collections:")
    for names in collections_list:
        names_list.append(names)
        print(names)
    return names_list


# returns all cve with the corresponding cvss
@app.get("/cve")
def list_items(db=Depends(get_collection)):
    items = list(db.find({}, {"_id": 0, "cve_id": 1, "cvss": 1}).sort("cve_id"))
    return items


# can take a cve id as input
@app.get("/cve/{cve_id}")
def read_item(cve_id: str, db=Depends(get_collection)):
    result = list(db.find({"cve_id": cve_id},
                          {"_id": 0, "cve_id": 1, "url": 1, "published": 1, "lastModified": 1, "cvss": 1, "patch": 1}))
    if result:
        return result
    else:
        raise HTTPException(status_code=404, detail="CVE not found.")


# can take cvss as input
@app.get("/cvss/{cvss}")
def read_item(cvss: float, db=Depends(get_collection)):
    result = list(db.find({"cvss": cvss},
                          {"_id": 0, "cve_id": 1, "url": 1, "published": 1, "lastModified": 1, "cvss": 1, "patch": 1}))
    if result:
        return result
    else:
        raise HTTPException(status_code=404, detail="CVSS not found.")


# returns the given diff from a specific cve id
@app.get("/cve/diff/{cve_id}")
def read_item(cve_id: str, db=Depends(get_diff_collection)):
    result = list(db.find({"cve_id": cve_id}, {"_id": 0, "commit_info": 1}))
    if result:
        return result
    else:
        raise HTTPException(status_code=404, detail="CVE not found.")


if __name__ == "__main__":
    # server which fastapi runs on and can be connected to
    import uvicorn

    uvicorn.run(app, host="localhost", port=8000)
