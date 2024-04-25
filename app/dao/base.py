from sqlalchemy import insert, select, delete

from app.booking.models import Bookings
from app.database import async_session_maker


class BaseDAO:
    model = None

    @classmethod
    async def find_by_id(cls, model_id: int):
        async with async_session_maker() as session:
            query = select(cls.model).filter_by(id=model_id)
            result = await session.execute(query)
            return result.scalar_one_or_none()

    @classmethod  # Позволяет вызывать метод без создания класса
    async def find_one_or_none(cls, **filter_by):
        async with async_session_maker() as session:
            query = select(cls.model).filter_by(**filter_by)  # SELECT * FROM bookings;
            bookings = await session.execute(query)
            # return result.scalars().all() # Конвертирует в json, вызывается 1 раз
            return bookings.scalar_one_or_none()

    @classmethod
    async def find_all(cls, **filter_by):
        async with async_session_maker() as session:
            query = select(cls.model).filter_by(**filter_by)  # SELECT * FROM bookings;
            bookings = await session.execute(query)
            return bookings.scalars().all()  # Конвертирует в json, вызывается 1 раз
            # return bookings.mappings().all() # Тоже самое но без странностей

    @classmethod
    async def add(cls, **data):
        async with async_session_maker() as session:
            query = insert(cls.model).values(**data)
            await session.execute(query)
            await session.commit()

    @classmethod
    async def delete(cls, model_id):
        async with async_session_maker() as session:
            query = delete(cls.model).filter_by(id=model_id)
            await session.execute(query)
            await session.commit()
