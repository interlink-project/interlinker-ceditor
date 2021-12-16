from fastapi import FastAPI, Request, HTTPException, status, Body
from fastapi.responses import JSONResponse, RedirectResponse
from fastapi.encoders import jsonable_encoder
from app.config import settings
from starlette.middleware.cors import CORSMiddleware
from app.database import db
from fastapi.responses import RedirectResponse
import os
from fastapi import File, UploadFile, APIRouter
from app.etherpad import *
from app.model import AssetCreate
import json
import random
import string
import requests
import uuid


ROOT_PATH = "/etherwrapper"

app = FastAPI(
    title="Etherpad API Wrapper", openapi_url=f"/openapi.json", docs_url="/docs", root_path=ROOT_PATH
)

# Set all CORS enabled origins
if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        # localhost only
        allow_methods=["*"],
        allow_headers=["*"],
    )

"""
from fastapi_utils.tasks import repeat_every
@app.on_event("startup")
@repeat_every(seconds=60 * 60)  # 1 hour
def repetitive_task() -> None:
    pass
    # clean(db)
"""

mainrouter = APIRouter()

@mainrouter.get("/")
def main():
    return RedirectResponse(url=f"{ROOT_PATH}/docs")

@mainrouter.get("/healthcheck")
def healthcheck():
    return True

specificrouter = APIRouter()

@specificrouter.get("/pads", response_description="Get real pads")
async def get_real_pads():
    response = requests.get(listAllPads)
    data = json.loads(response._content)
    data = data["data"]["padIDs"]
    for i in data:
        print(i)
        requests.get(deletePad(i))
    return JSONResponse(status_code=status.HTTP_200_OK, content=data)

@specificrouter.get("/pads/delete", response_description="Delete unused pads")
async def delete_unused_pads():
    assets = await db["assets"].find().to_list(1000)
    response = requests.get(listAllPads)
    data = json.loads(response._content)
    data = data["data"]["padIDs"]
    matches = [asset["_id"] for asset in assets if asset["padID"] not in data]
    for id in matches:
        db["assets"].delete_one({"_id": id})
    return JSONResponse(status_code=status.HTTP_200_OK, content=data)

@specificrouter.get("/pads/clean", response_description="Delete all pads")
async def delete_all_pads():
    assets = await db["assets"].find().to_list(1000)
    for asset in assets:
        requests.get(deletePad(asset["padID"]))
        db["assets"].delete_one({"_id": asset["_id"]})

    return JSONResponse(status_code=status.HTTP_200_OK)

defaultrouter = APIRouter()

async def create_pad(name):
    groupMapper = ''.join(random.choice(string.ascii_lowercase) for i in range(10))
    response = requests.get(createGroupIfNotExistsFor(groupMapper=groupMapper))
    data = json.loads(response._content)
    print(data)
    groupID = data["data"]["groupID"]
    response = requests.get(createGroupPad(groupID=groupID, padName=name))
    data = json.loads(response._content)
    print(data)
    padID = data["data"]["padID"]

    asset = {
        "_id": uuid.uuid4().hex,
        "groupMapper": groupMapper,
        "name": name,
        "groupID": groupID,
        "padID": padID
    }
    asset = jsonable_encoder(asset)
    new_asset = await db["assets"].insert_one(asset)
    return await db["assets"].find_one({"_id": new_asset.inserted_id})


@defaultrouter.post("/assets/", response_description="Add new asset")
async def create_asset(asset_in: AssetCreate = Body(...)):
    created_asset = await create_pad(asset_in.name)
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=created_asset)


@defaultrouter.get(
    "/assets/", response_description="List all assets"
)
async def list_assets():
    assets = await db["assets"].find().to_list(1000)
    return JSONResponse(status_code=status.HTTP_200_OK, content=assets)


@defaultrouter.get(
    "/assets/{id}", response_description="Get a single asset"
)
async def show_asset(id: str):
    if (asset := await db["assets"].find_one({"_id": id})) is not None:
            return JSONResponse(status_code=status.HTTP_200_OK, content=asset)

    raise HTTPException(status_code=404, detail="Asset {id} not found")

@defaultrouter.post(
    "/assets/{id}/clone", response_description="Clone specific asset"
)
async def clone_asset(id: str):
    if (asset := await db["assets"].find_one({"_id": id})) is not None:
        original_name = asset["name"]
        created_asset = await create_pad(f"Copy of {original_name}")
        response = requests.get(getHTML(padID=asset["padID"]))
        data = json.loads(response._content)
        html = data["data"]["html"]
        
        print(f"Setting html {html}")
        requests.get(setHTML(padID=created_asset["padID"], html=html))
        # response = requests.get(getHTML(padID=created_asset["padID"]))
        # data = json.loads(response._content)
        # print(data)
        return JSONResponse(status_code=status.HTTP_201_CREATED, content=created_asset)

    raise HTTPException(status_code=404, detail="Asset {id} not found")


@defaultrouter.delete("/assets/{id}", response_description="Delete a asset")
async def delete_asset(id: str):
    if (asset := await db["assets"].find_one({"_id": id})) is not None:
        response = requests.get(deletePad(padID=asset["padID"]))
        data = json.loads(response._content)
        print(data)
        delete_result = await db["assets"].delete_one({"_id": id})
        if delete_result.deleted_count == 1:
            return JSONResponse(status_code=status.HTTP_204_NO_CONTENT)
        return HTTPException(status_code=503, detail="Error while deleting")

    raise HTTPException(status_code=404, detail="Asset {id} not found")


from fastapi.templating import Jinja2Templates
templates = Jinja2Templates(directory="templates")

@defaultrouter.get(
    "/assets/{id}/gui", response_description="GUI for specific asset"
)
async def gui_asset(request: Request, id: str):
    if (asset := await db["assets"].find_one({"_id": id})) is not None:
        response = requests.get("http://proxy/auth/api/v1/users/me", headers=request.headers)
        current_user = json.loads(response._content)

        try:
            email = current_user["email"]
        except:
            print(response)
            return RedirectResponse(f"/auth/login?redirect_on_callback=/etherwrapper/api/v1/assets/{id}/gui")
            # raise HTTPException(status_code=401, detail="You are not logged in")
            # email = "AnonymousUser"
        response = requests.get(createAuthorIfNotExistsFor(
            authorName=email, authorMapper=email))
        data = json.loads(response._content)
        authorID = data["data"]["authorID"]
        response = requests.get(createSession(groupID=asset["groupID"],
                                authorID=authorID, validUntil=2022201246))
        data = json.loads(response._content)
        sessionID = data["data"]["sessionID"]

        url = iframeUrl(sessionID, asset["groupID"], asset["name"])
        response = templates.TemplateResponse(
            "index.html", {"request": request, "url": url})
        return response

    raise HTTPException(status_code=404, detail="Asset {id} not found")


app.include_router(defaultrouter, prefix=settings.API_V1_STR, tags=["default"])
app.include_router(specificrouter, prefix=settings.API_V1_STR, tags=["specific"])
app.include_router(mainrouter, tags=["main"])