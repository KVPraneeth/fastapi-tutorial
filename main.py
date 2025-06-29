from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def read_root():
    return {"message": "Hello World"}


# @app.get("/items/{item_id}") ## Path parameter - in browser, this will be /items/{value} Ex --> /items/1, /items/2, etc.
# def read_item(item_id):
#     return {"item_id": item_id}


@app.get("/items/{it}")
def read_item(it: int):
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


class Idname(str, Enum):
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
        return {
            "name": "Venu",
            "detail": "Father",
            "note": "Using value directly for comparison",
        }
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
async def read_fake_names(
    skip: int = 0, limit: int = 10
):  # we are providing default values for skip and limit
    return fake_names_db[skip : skip + limit]


# Optional query parameters
@app.get("/fake_names_optional/")
async def read_fake_names_optional(skip: int = 0, limit: int = 10, name: str = None):
    if name:
        return [fake_name for fake_name in fake_names_db if fake_name["name"] == name][
            skip : skip + limit
        ]
    return fake_names_db[skip : skip + limit]


# Multiple path and query parameters

items = [
    {"item_id": 1, "name": "Bat"},
    {"item_id": 2, "name": "Ball"},
    {"item_id": 3, "name": "Football"},
]


@app.get("/items_bought/{name_id}/items/{item_id}")
async def cart_items(name_id: Idname, item_id: int, qty: int = 1, price: float = None):

    # find item based on item_id in items list
    item = next((item for item in items if item["item_id"] == item_id), None)
    if item is None:
        return {"error": "Item nor found"}

    response = {
        "buyer": name_id.value,
        "item_id": item_id,
        "item": item["name"],
        "qty": qty,
    }

    if price:
        response["price"] = price
    return response


# Request body - we use pydantic models to define the request body

from pydantic import BaseModel


class Item(BaseModel):
    id: int
    name: str
    price: float
    quantity: int = 1
    discount: float | None = None


@app.post("/items/")
async def create_item(item: Item):
    return item


# request bodty with path and query parameters


@app.post("/items/{item_id}")
async def create_item_with_path(item_id: int, item: Item):
    return {
        "item_id": item_id,
        "item": item,
    }


# Additional validation

from typing import Annotated

from fastapi import Query


@app.get("/items_with_validation/")
async def read_items_with_validation(
    item_id: int,
    q: Annotated[str | None, Query(max_length=50)] = None,
    skip: int = 0,
    limit: int = 10,
):
    if q:
        return {"item_id": item_id, "q": q, "skip": skip, "limit": limit}
    return {"item_id": item_id, "skip": skip, "limit": limit}


# non-Annotated


@app.get("/items_with_validation_non_annotated/")
async def read_items_with_validation_non_annotated(
    item_id: int,
    q: str | None = Query(
        default=None, match_length=50
    ),  # Using Query directly without Annotated
    skip: int = 0,
    limit: int = 10,
):
    if q:
        return {"item_id": item_id, "q": q, "skip": skip, "limit": limit}
    return {"item_id": item_id, "skip": skip, "limit": limit}


# Query parameter list/ multiple values - Ex /items_with_list/?q=1&q=2&q=3

items = ["bat", "ball", "football", "tennis ball", "cricket bat"]


@app.get("/items_with_list/")
async def read_items_with_list(q: Annotated[list[str] | None, Query()] = None):
    query_items = {item: item for item in items if not q or item in q}
    return query_items


# deprecated parameters - These are parameters that are no longer recommended for use and may be removed in future versions of the API.
# Exclude parameters from the OpenAPI schema using `include_in_schema=False` and mark them as deprecated using `deprecated=True`.


@app.get("/items_with_deprecated/")
async def read_items_with_deprecated(
    item_id: int,
    q: Annotated[str | None, Query(max_legth=10)] = "Its a product",
    qty: Annotated[int, Query(deprecated=True)] = 1,
    stock: Annotated[int, Query(include_in_schema=False, deprecated=True)] = 1000,
):
    return {
        "item_id": item_id,
        "q": q,
        "qty": qty,
        "message": "qty is deprecated, use quantity instead",
    }
