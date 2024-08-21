from sqlalchemy import (
    and_,
    delete,
    insert,
    select,
)

from app.core.database import async_session_maker


class BaseRepository:
    model = None

    @classmethod
    async def find_by_id(cls, model_id: int):
        async with async_session_maker() as session:
            query = select(cls.model).filter_by(id=model_id)
            result = await session.execute(query)
            return result.scalar_one_or_none()

    @classmethod
    async def find_by_filter(cls, **filter_by):
        async with async_session_maker() as session:
            query = select(cls.model).filter_by(**filter_by)
            result = await session.execute(query)
            return result.scalars().all()

    @classmethod
    async def find_one_or_none(cls, **filter_by):
        async with async_session_maker() as session:
            query = select(cls.model).filter_by(**filter_by)
            result = await session.execute(query)
            return result.scalar_one_or_none()

    @classmethod
    async def add(cls, **data):
        async with async_session_maker() as session:
            query = insert(cls.model).values(**data)
            await session.execute(query)
            await session.commit()

    @classmethod
    async def remove_by_id(cls, model_id: int):
        async with async_session_maker() as session:
            query = delete(cls.model).where(cls.model.id == model_id)
            await session.execute(query)
            await session.commit()

    @classmethod
    async def remove_by_filter(cls, **filter_by):
        async with async_session_maker() as session:
            async with session.begin():
                conditions = [
                    getattr(cls.model, key) == value for key, value in filter_by.items()
                ]
                query = delete(cls.model).where(and_(*conditions))
                result = await session.execute(query)
                return result.rowcount if result else 0
