from sqlalchemy import select

from app.dao.base_dao import BaseDAO
from app.database import async_session
from app.users.models import User


class UserDAO(BaseDAO):
    model = User
    child_model = User.role

    @classmethod
    async def find_user(cls, model_username: str):
        async with async_session() as session:
            query = select(cls.model.__table__.columns).where(
                cls.model.username == model_username
            )
            res = await session.execute(query)
            return res.mappings().one_or_none()
