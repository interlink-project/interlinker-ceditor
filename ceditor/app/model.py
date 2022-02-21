from pydantic import BaseModel, Field, validator
import datetime
from typing import Optional
from app.config import settings

class AssetCreateSchema(BaseModel):
    name: str = Field(...)

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        schema_extra = {
            "example": {
                "name": "Example name",
            }
        }


class AssetSchema(AssetCreateSchema):
    name: str
    created_at: datetime.datetime
    updated_at: Optional[datetime.datetime]
    
    class Config:
        allow_population_by_field_name = True

class AssetBasicDataSchema(BaseModel):
    # id: str = Field(alias='_id')
    name: str
    icon: str = "https://avatars.githubusercontent.com/u/19719052?s=88&v=4"
    createdTime: datetime.datetime = Field(alias='created_at')
    modifiedTime: Optional[datetime.datetime] = Field(alias='updated_at')

    class Config:
        allow_population_by_field_name = True

    """
    @validator('viewLink', always=True)
    def view_link(cls, name, values):
        asset_id = values["id"]
        return settings.COMPLETE_SERVER_NAME + f"/assets/{asset_id}/view"
        
    @validator('cloneLink', always=True)
    def clone_link(cls, name, values):
        asset_id = values["id"]
        return settings.COMPLETE_SERVER_NAME + f"/assets/{asset_id}/clone"
    
    viewLink: Optional[str]
    editLink: Optional[str]
    cloneLink: Optional[str]
    """