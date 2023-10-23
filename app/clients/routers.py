from fastapi import APIRouter, Depends
from fastapi_cache.decorator import cache
from pydantic import TypeAdapter

from app.clients.dao import ClinetDAO
from app.clients.schemas import ClientSchem, CreateClient
from app.users.auth import get_current_user
from app.users.models import User

router = APIRouter(prefix="/api/v1/client", tags=["Контрагенты"])


@router.get("/")
@cache(expire=120)
async def get_all_clients(
    current_user: User = Depends(get_current_user),
) -> list[ClientSchem]:
    clients = await ClinetDAO.find_all()
    ta = TypeAdapter(list[ClientSchem])
    clients_json = ta.validate_python(clients)
    return clients_json


@router.get("/{client_id}")
async def get_client_by_id(
    client_id: int, current_user: User = Depends(get_current_user)
) -> ClientSchem:
    return await ClinetDAO.find_by_id(client_id)


@router.post("/")
async def create_client(
    client: CreateClient, current_user: User = Depends(get_current_user)
):
    return await ClinetDAO.add(client)


@router.put("/{client_id}")
async def update_client(
    client_id: int, client: CreateClient, current_user: User = Depends(get_current_user)
):
    return await ClinetDAO.update(client_id, client)


@router.delete("/{client_id}")
async def delete_client(client_id: int, current_user: User = Depends(get_current_user)):
    return await ClinetDAO.delete(client_id)
