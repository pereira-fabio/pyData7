from pymongo import MongoClient
from fastapi import FastAPI, HTTPException, Depends

# Connecting to the database
hostname = "localhost"
port = 27017
user = "root"
password = "example"
connection = MongoClient(hostname, port, username=user, password=password)

app = FastAPI()


def get_database():
    db = connection["pydata7"]
    return db


def get_collection(collection_name: str, db=Depends(get_database)):
    return db[collection_name]


def get_diff_collection(db=Depends(get_database)):
    return db["commit_diff"]


@app.get("/")
def read_root():
    return {"message": "Hello,FastAPI"}


@app.get("/collections")
def get_collections(db=Depends(get_database)):
    names_list = []
    collections_list = db.list_collection_names()
    print("Available Collections:")
    for names in collections_list:
        names_list.append(names)
        print(names)
    return names_list


@app.get("/cve")
def list_items(db=Depends(get_collection)):
    items = list(db.find({}, {"_id": 0, "cve_id": 1, "cvss": 1}).sort("cve_id"))
    return items


@app.get("/cve/{cve_id}")
def read_item(cve_id: str, db=Depends(get_collection)):
    result = list(db.find({"cve_id": cve_id},
                          {"_id": 0, "cve_id": 1, "url": 1, "published": 1, "lastModified": 1, "cvss": 1, "patch": 1}))
    if result:
        return result
    else:
        raise HTTPException(status_code=404, detail="CVE not found.")


@app.get("/cvss/{cvss}")
def read_item(cvss: float, db=Depends(get_collection)):
    result = list(db.find({"cvss": cvss},
                          {"_id": 0, "cve_id": 1, "url": 1, "published": 1, "lastModified": 1, "cvss": 1, "patch": 1}))
    if result:
        return result
    else:
        raise HTTPException(status_code=404, detail="CVSS not found.")


@app.get("/cve/diff/{cve_id}")
def read_item(cve_id: str, db=Depends(get_diff_collection)):
    result = list(db.find({"cve_id": cve_id}, {"_id": 0, "commit_info": 1}))
    if result:
        return result
    else:
        raise HTTPException(status_code=404, detail="CVE not found.")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="localhost", port=8000)
