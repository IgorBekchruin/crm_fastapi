from sqlalchemy import select

from app.dao.base_dao import BaseDAO
from app.database import async_session
from app.orders.models import Order


class OrderDAO(BaseDAO):
    model = Order
    child_model = Order.user

    @classmethod
    async def get_all_orders_by_user_id(cls, model_column_id: int):
        async with async_session() as session:
            query = select(cls.model).filter_by(user_id=model_column_id)
            res = await session.execute(query)
            return res.scalars().all()
