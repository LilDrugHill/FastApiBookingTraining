# DATA access objects
from datetime import date

from fastapi import Depends
from sqlalchemy import select, and_, or_, insert
from sqlalchemy.sql.functions import count

from app.booking.models import Bookings
from app.dao.base import BaseDAO
from app.database import engine, async_session_maker
from app.hotels.rooms.models import Rooms
from app.users.dependencies import get_current_user
from app.users.models import Users


class BookingDAO(BaseDAO):
    model = Bookings

    # @classmethod # Позволяет вызывать метод без создания класса
    # async def find_all(cls):
    #     async with async_session_maker() as session:
    #         query = select(Bookings) # SELECT * FROM bookings;
    #         bookings = await session.execute(query)
    #         # return result.scalars().all() # Конвертирует в json, вызывается 1 раз
    #         return bookings.mappings().all() # Тоже самое но без странностей
    @classmethod
    async def add(
            cls,
            user_id: int,
            room_id: int,
            date_from: date,
            date_to: date,
    ):
        """
        with booked_rooms as (
        select * from bookings
         where room_id = 1 and
          (date_from >= '2023-05-15' and date_from <= '2023-06-20') or
          (date_from <= '2023-05-15' and date_to > '2023-05-15'))
        """
        async with async_session_maker() as session:
            booked_rooms = select(Bookings).where(
                and_(
                    Bookings.room_id == 1,
                    or_(
                        and_(
                            Bookings.date_from >= date_from,
                            Bookings.date_from <= date_to
                        ),
                        and_(
                            Bookings.date_from <= date_from,
                            Bookings.date_to > date_from
                        )
                    )
                )
            ).cte('booked_rooms') # cte создает имя в области видимости sql запросов
            """
            select rooms.quantity - count(booked_rooms.room_id) as free_rooms_count from rooms
            left join booked_rooms on booked_rooms.room_id = rooms.id
            where rooms.id = 1
            group by rooms.quantity, rooms.id;
            """
            get_rooms_left = select(
                Rooms.quantity - count(booked_rooms.c.room_id).label('rooms_left')
            ).select_from(Rooms).join(
                booked_rooms, booked_rooms.c.room_id == Rooms.id, isouter=True
            ).where(Rooms.id == 1).group_by(
                Rooms.quantity, booked_rooms.c.room_id
            )

            # print(rooms_left.compile(engine, compile_kwargs={'literal_binds': True}))

            rooms_left = await session.execute(get_rooms_left)
            rooms_left: int = rooms_left.scalar()

            if rooms_left > 0:
                get_price = select(Rooms.price).filter_by(id=room_id)
                price = await session.execute(get_price)
                price: int = price.scalar()
                add_booking = insert(Bookings).values(
                    room_id=room_id,
                    user_id=user_id,
                    date_from=date_from,
                    date_to=date_to,
                    price=price,
                ).returning(Bookings)

                new_booking = await session.execute(add_booking)
                await session.commit()
                return new_booking.scalar()

            else:
                return None



