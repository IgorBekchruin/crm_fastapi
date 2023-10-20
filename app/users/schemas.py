from typing import Optional
from pydantic import BaseModel, ConfigDict


class UserSchem(BaseModel):
    username: str
    password: str

    model_config = ConfigDict(from_attributes=True)


class UserCreate(BaseModel):
    username: str
    password: str

    model_config = ConfigDict(from_attributes=True)


class UserSave(BaseModel):
    username: str
    hashed_password: str

    model_config = ConfigDict(from_attributes=True)