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


@app.get("/db")
def coll():
    return get_database()


@app.get("/")
def read_root():
    return {"message": "Hello,FastAPI"}


@app.get("/CVE")
def list_items(db=Depends(get_collection)):
    items = list(db.find({}, {"_id": 0, "cve_id": 1}))
    # print(items)
    return items


@app.get("/CVE/{cve_id}")
def read_item(cve_id: str, db=Depends(get_collection)):
    result = list(db.find({"cve_id": cve_id}, {"_id": 0, "cve_id": 1, "url": 1, "cvss": 1}))
    print(result)
    if result:
        return result
    else:
        raise HTTPException(status_code=404, detail="CVE not found")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="localhost", port=8000)
