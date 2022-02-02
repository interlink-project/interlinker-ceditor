import datetime
import json
import random
import string
import uuid

import requests
from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder

from app.etherpad import *
from app.model import AssetCreateSchema


async def create_pad(collection, name):
    if not name or name == "":
        raise HTTPException(status_code=400, detail="Invalid name")
    groupMapper = ''.join(random.choice(string.ascii_lowercase) for i in range(10))
    response = requests.get(createGroupIfNotExistsFor(groupMapper=groupMapper)).json()
    groupID = response["data"]["groupID"]
    response = requests.get(createGroupPad(groupID=groupID, padName=name)).json()
    padID = response["data"]["padID"]
    print(f"Created pad {padID} for {groupID}")

    asset = {
        "_id": uuid.uuid4().hex,
        "created_at": datetime.datetime.now(),
        "groupMapper": groupMapper,
        "name": name,
        "groupID": groupID,
        "padID": padID
    }
    print(asset)
    asset = jsonable_encoder(asset)
    new_asset = await collection.insert_one(asset)
    return await get(collection, new_asset.inserted_id)


async def get(collection, id: str):
    return await collection.find_one({"_id": id})


async def get_all(collection):
    return await collection.find().to_list(1000)


async def create(collection, asset: AssetCreateSchema):
    return await create_pad(collection, asset.name)


async def clone(collection, asset):
    data_copy = AssetCreateSchema(**asset)
    print(data_copy)
    created_asset = await create(collection, data_copy)
    response = requests.get(getHTML(padID=asset["padID"])).json()
    html = response["data"]["html"]

    print(f"Setting html {html}")
    requests.get(setHTML(padID=created_asset["padID"], html=html))
    return created_asset


async def update(collection, id: str, data):
    data["updated_at"] = datetime.datetime.now()
    await collection.update_one({"_id": id}, {"$set": data})
    return await get(collection, id)


async def delete(collection, asset):
    response = requests.get(deletePad(padID=asset["padID"])).json()
    data = json.loads(response._content)
    print(data)
    return await collection.delete_one({"_id": asset["_id"]})
