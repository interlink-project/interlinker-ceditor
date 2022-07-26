import json
import os

import time
import uuid
from typing import Optional

import requests
from fastapi import (
    APIRouter,
    Body,
    Cookie,
    Depends,
    FastAPI,
    HTTPException,
    Request,
    status,
)
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.middleware.cors import CORSMiddleware
from starlette.status import HTTP_422_UNPROCESSABLE_ENTITY

from app.authentication import get_current_active_user, get_current_user
from app.config import settings
from app.database import (
    AsyncIOMotorCollection,
    close_mongo_connection,
    connect_to_mongo,
    get_collection,
)
from app.errors import http_422_error_handler
from app.etherpad import *
from app.model import AssetCreateSchema, AssetSchema, AssetBasicDataSchema
from app import crud

domainfo = {
        "PROTOCOL": settings.PROTOCOL,
        "SERVER_NAME": settings.SERVER_NAME ,
        "BASE_PATH": settings.BASE_PATH ,
        "COMPLETE_SERVER_NAME": settings.COMPLETE_SERVER_NAME 
    }
app = FastAPI(
    title="Collaborative Editor API", openapi_url=f"/openapi.json", docs_url="/docs", root_path=settings.BASE_PATH
)
app.add_event_handler("startup", connect_to_mongo)
app.add_event_handler("shutdown", close_mongo_connection)


templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

# Set all CORS enabled origins
if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_methods=["*"],
        allow_headers=["*"],
    )

mainrouter = APIRouter()


@mainrouter.get("/")
def main():
    return RedirectResponse(url=f"{settings.BASE_PATH}/docs")


@mainrouter.get("/healthcheck")
def healthcheck():
    return True


integrablerouter = APIRouter()


@integrablerouter.post("/assets", response_description="Add new asset", response_model=AssetSchema)
async def create_asset(asset_in: AssetCreateSchema = Body(...), collection: AsyncIOMotorCollection = Depends(get_collection)):
    created_asset = await crud.create(collection=collection, asset=asset_in)
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=created_asset)


@integrablerouter.get(
    "/assets/instantiate", response_description="GUI for asset creation"
)
async def instantiate_asset(request: Request):
    return templates.TemplateResponse("instantiator.html", {"request": request, "BASE_PATH": settings.BASE_PATH, "DOMAIN_INFO": json.dumps(domainfo)})


@integrablerouter.get(
    "/assets/{id}", response_description="Asset JSON", response_model=AssetBasicDataSchema
)
async def asset_data(id: str, collection: AsyncIOMotorCollection = Depends(get_collection)):
    if (asset := await crud.get(collection, id)) is not None:
        return asset

    raise HTTPException(status_code=404, detail="Asset {id} not found")


@integrablerouter.delete("/assets/{id}", response_description="No content")
async def delete_asset(id: str, collection: AsyncIOMotorCollection = Depends(get_collection)):
    if (asset := await crud.get(collection, id)) is not None:
        delete_result = await crud.delete(collection, asset)
        if delete_result.deleted_count == 1:
            return HTTPException(status_code=status.HTTP_204_NO_CONTENT)
        return HTTPException(status_code=503, detail="Error while deleting")

    raise HTTPException(status_code=404, detail="Asset {id} not found")


@integrablerouter.get(
    "/assets/{id}/view", response_description="GUI for interaction with asset"
)
async def asset_viewer(request: Request, id: str, current_user: dict = Depends(get_current_active_user), collection: AsyncIOMotorCollection = Depends(get_collection), sessionID: Optional[str] = Cookie(None)):
    if (asset := await crud.get(collection, id)) is not None:
        user_id = current_user["sub"]
        email = current_user["email"]

        # TODO: check if user has access to this resource
        print(email)
        response = requests.get(createAuthorIfNotExistsFor(
            authorName=email, authorMapper=user_id))
        data = json.loads(response._content)
        authorID = data["data"]["authorID"]

        valid_until = int(time.time()) + 5 * 60 * 60  # 5 hours from now
        response = requests.get(createSession(groupID=asset["groupID"],
                                authorID=authorID, validUntil=valid_until))
        data = json.loads(response._content)
        session_id = data["data"]["sessionID"]
        print(f"Session for {authorID}: {session_id}")
        url = iframeUrl(asset["padID"])
        response = templates.TemplateResponse(
            "gui.html", {"request": request, "url": url})

        # TODO: sessionID cookie can container session IDS separated by commas, so it would be nice to check if any of the current sessions is valid for this pad
        response.set_cookie(
            key="sessionID",
            value=session_id,
            # TODO: if https, true
            secure=False
        )
        return response

    raise HTTPException(status_code=404, detail="Asset {id} not found")


@integrablerouter.post(
    "/assets/{id}/clone", response_description="Asset JSON", response_model=AssetBasicDataSchema
)
async def clone_asset(id: str, collection: AsyncIOMotorCollection = Depends(get_collection)):
    if (asset := await crud.get(collection, id)) is not None:
        created_asset = await crud.clone(collection, asset)
        return JSONResponse(status_code=status.HTTP_201_CREATED, content=created_asset)

    raise HTTPException(status_code=404, detail="Asset {id} not found")

customrouter = APIRouter()


@customrouter.get("/pads", response_description="Get real pads")
async def get_real_pads():
    response = requests.get(listAllPads).json()
    data = response["data"]["padIDs"]
    for i in data:
        print(i)
        requests.get(deletePad(i))
    return JSONResponse(status_code=status.HTTP_200_OK, content=data)


@customrouter.get("/pads/delete", response_description="Delete unused pads")
async def delete_unused_pads(collection: AsyncIOMotorCollection = Depends(get_collection)):
    assets = await collection.find().to_list(1000)
    response = requests.get(listAllPads).json()
    data = response["data"]["padIDs"]
    matches = [asset["_id"] for asset in assets if asset["padID"] not in data]
    for id in matches:
        collection.delete_one({"_id": id})
    return JSONResponse(status_code=status.HTTP_200_OK, content=data)


@customrouter.get("/pads/clean", response_description="Delete all pads")
async def delete_all_pads(collection: AsyncIOMotorCollection = Depends(get_collection)):
    assets = await collection.find().to_list(1000)
    for asset in assets:
        requests.get(deletePad(asset["padID"]))
        collection.delete_one({"_id": asset["_id"]})

    return JSONResponse(status_code=status.HTTP_200_OK)



@customrouter.get(
    "/assets", response_description="List all assets"
)
async def list_assets(collection: AsyncIOMotorCollection = Depends(get_collection)):
    assets = await collection.find().to_list(1000)
    return JSONResponse(status_code=status.HTTP_200_OK, content=assets)


app.include_router(mainrouter, tags=["main"])
app.include_router(integrablerouter, tags=["Integrable"])
app.include_router(customrouter, prefix=settings.API_V1_STR, tags=["Custom endpoints"])


app.add_exception_handler(HTTP_422_UNPROCESSABLE_ENTITY, http_422_error_handler)
