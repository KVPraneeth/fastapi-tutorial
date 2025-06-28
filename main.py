from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello World"}

# @app.get("/items/{item_id}") ## Path parameter - in browser, this will be /items/{value} Ex --> /items/1, /items/2, etc.
# def read_item(item_id):
#     return {"item_id": item_id}

@app.get("/items/{it}")
def read_item(it:int):
    return {"item_id": it}


## Order matters in path operations

@app.get("/users/me")
async def read_current_user():
    return {"User": "Praneeth"}

@app.get("/users/{user_id}")
async def read_user(user_id: int):
    return {"user_id": user_id}


# For predefined values in path parameters, use Enum
from enum import Enum

class Idname(str,Enum):
    id_1 = "Praneeth"
    id_2 = "Rohit"
    id_3 = "Venu"
    id_4 = "Jyothi"

@app.get("/names/{name_id}")
async def read_name(name_id: Idname):
    if name_id == Idname.id_1:
        return {"name": "Praneeth"}
    if name_id == Idname.id_2:
        return {"name": "Rohit"}
    if name_id.value == "Venu":
        return {"name": "Venu","detail": "Father" ,"note": "Using value directly for comparison"}
    if name_id == Idname.id_4:
        return {"name": "Jyothi"}
    return {"error": "Name not found"}

# path as path parameter

from fastapi import Path

@app.get("/files/{file_path:path}")
async def read_file(file_path: str = Path(...)):
    return {"file_path": file_path}

# Query parameters

fake_names_db = [{"name": "Sam"}, {"name": "Pam"}, {"name": "Dam"}, {"name": "Bam"}]

@app.get("/fake_names/")
async def read_fake_names(skip: int  = 0, limit: int = 10): # we are providing default values for skip and limit
    return fake_names_db[skip: skip + limit]

# Optional query parameters
@app.get("/fake_names_optional/")
async def read_fake_names_optional(skip: int = 0, limit: int = 10, name: str = None):
    if name:
        return [fake_name for fake_name in fake_names_db if fake_name["name"] == name][skip: skip + limit]
    return fake_names_db[skip: skip + limit]