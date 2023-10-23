from sqlalchemy import delete, desc, insert, select, update
from sqlalchemy.orm import joinedload

from app.database import async_session


class BaseDAO:
    model = None
    child_model = None

    @classmethod
    async def find_all(cls, limit: int = 20):
        async with async_session() as session:
            query = (
                select(cls.model)
                .options(joinedload(cls.child_model))
                .limit(limit)
                .order_by(desc(cls.model.id))
            )
            res = await session.execute(query)
            return res.scalars().unique().all()

    @classmethod
    async def find_by_id(cls, model_id: int):
        async with async_session() as session:
            query = (
                select(cls.model)
                .options(joinedload(cls.child_model))
                .filter_by(id=model_id)
            )
            res = await session.execute(query)
            return res.scalars().unique().one_or_none()

    @classmethod
    async def find_by_name(cls, model_name: str):
        async with async_session() as session:
            query = (
                select(cls.model)
                .options(joinedload(cls.child_model))
                .filter_by(name=model_name)
            )
            res = await session.execute(query)
            return res.scalars().unique().one_or_none()

    @classmethod
    async def add(cls, data):
        async with async_session() as session:
            stm = insert(cls.model).values(**data.dict())
            await session.execute(stm)
            await session.commit()
            return {"status_code": "200", "msg": "success"}

    @classmethod
    async def update(cls, model_id: int, data):
        async with async_session() as session:
            stmt = (
                update(cls.model).where(cls.model.id == model_id).values(**data.dict())
            )
            await session.execute(stmt)
            await session.commit()
            return {"status_code": "200", "msg": "success"}

    @classmethod
    async def delete(cls, model_id: int):
        async with async_session() as session:
            stmt = delete(cls.model).where(cls.model.id == model_id)
            await session.execute(stmt)
            await session.commit()
            return {"status_code": "200", "msg": "success"}
