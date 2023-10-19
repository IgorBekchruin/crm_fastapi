from fastapi import APIRouter, Depends
from pydantic import TypeAdapter

from app.orders.dao import OrderDAO
from app.orders.schemas import OrderSchem
from app.users.auth import get_current_user
from app.users.models import User
from fastapi_cache.decorator import cache


router = APIRouter(
    prefix='/api/v1/orders',
    tags=['Заказы']
)


@router.get('/')
@cache(expire=60)
async def get_all_orders(
    current_user: User = Depends(get_current_user)
) -> list[OrderSchem]:
    orders = await OrderDAO.find_all()
    ta = TypeAdapter(list[OrderSchem])
    orders_json = ta.validate_python(orders)
    return orders_json


@router.get('/{order_id}')
async def get_order_by_id(
    order_id: int,
    current_user: User = Depends(get_current_user)
) -> OrderSchem:
    return await OrderDAO.find_by_id(order_id)


# @router.get('/{user_id}')
# async def get_orders_from_user(
#     user_id: int,
#     # current_user: User = Depends(get_current_user)
# ):
#     return await OrderDAO.get_all_orders_by_user_id(user_id)


@router.post('/')
async def create_orders(
    order: OrderSchem,
    current_user: User = Depends(get_current_user)
):
    return await OrderDAO.add(order)


@router.put('/{order_id}')
async def update_order(
    order_id: int,
    order: OrderSchem,
    current_user: User = Depends(get_current_user)
):
    return await OrderDAO.update(order_id, order)


@router.delete('/{order_id}')
async def delete_order(
    order_id: int,
    current_user: User = Depends(get_current_user)
):
    return await OrderDAO.delete(order_id)