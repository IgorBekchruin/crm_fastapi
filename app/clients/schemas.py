from datetime import datetime
from fastapi import Form

from pydantic import BaseModel, ConfigDict


class ClientSchem(BaseModel):
    name: str
    price: float
    production: str
    contact: str
    last_contact: datetime
    user_id: int

    model_config = ConfigDict(
        from_attributes=True,
        arbitrary_types_allowed=True)


class CreateClient(ClientSchem):
    pass


class UpdateClient(ClientSchem):
    id: int
