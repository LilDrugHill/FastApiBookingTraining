from datetime import date

from sqlalchemy import select, and_, or_
from sqlalchemy.sql.functions import coalesce, count

from app.booking.models import Bookings
from app.dao.base import BaseDAO
from app.database import async_session_maker
from app.hotels.models import Hotels
from app.hotels.rooms.models import Rooms


class HotelsDAO(BaseDAO):
    """
    get_all_rooms(cls, hotel_id)
    get_hotel_by_param(cls, location: str, date_form, date_to: date)
    """
    model = Hotels

    @classmethod
    async def get_hotel_rooms(cls, hotel_id: int, date_from: date, date_to: date):

        async with async_session_maker() as session:
            """
            with booked_rooms as (
            select bookings.room_id, count(bookings) from bookings 
            inner join rooms on bookings.room_id = rooms.id
            where rooms.hotel_id = 1 and
              (date_from >= '2023-05-15' and date_from <= '2023-06-20') or
              (date_from <= '2023-05-15' and date_to > '2023-05-15') 
            GROUP by bookings.room_id)       
            """
            booked_rooms = select(
                Bookings.room_id,
                count(Bookings.id)
            ).select_from(
                Bookings
            ).join(
                Rooms, Rooms.id == Bookings.room_id
            ).where(
                and_(
                    Hotels.id == hotel_id,
                    or_(
                        and_(Bookings.date_from >= date_from, Bookings.date_from <= date_to),
                        and_(Bookings.date_from <= date_from, Bookings.date_to > date_from)))
            ).group_by(
                Bookings.room_id
            ).cte('booked_rooms')

            """
            select 
                rooms.id, rooms.hotel_id, rooms.name, 
                rooms.description, rooms.services, rooms.price, 
                rooms.quantity, rooms.image_id, 
                (price * 5) as total_cost, 
                rooms.quantity - booked_rooms_count.count as rooms_left from rooms 
            left join booked_rooms_count on booked_rooms_count.room_id = rooms.id 
            where hotel_id = 1;
            """
            get_hotel_rooms = select(
                Rooms.id, Rooms.hotel_id, Rooms.name, Rooms.description,
                Rooms.services, Rooms.price, Rooms.quantity, Rooms.image_id,
                (Rooms.price * (date_to - date_from)).label('total_cost'),
                (Rooms.quantity - booked_rooms.c.count).label('rooms_left')
            ).select_from(
                Rooms
            ).join(
                booked_rooms, booked_rooms.c.room_id == Rooms.id
            ).where(
                Rooms.hotel_id == hotel_id)

            hotel_rooms = await session.execute(get_hotel_rooms)
            hotel_rooms: list[dict] = hotel_rooms.mappings().all()
            return hotel_rooms


    @classmethod
    async def get_hotel_by_param(cls, location: str, date_form, date_to: date):
        """

        Parameters
        ----------
        location
        date_form
        date_to

        Returns
        -------

        """
        async with async_session_maker() as session:
            """
            WITH booked_rooms AS (
                SELECT rooms.hotel_id
                FROM bookings
                LEFT JOIN rooms ON bookings.room_id = rooms.id
                WHERE (date_from >= '2023-05-15' AND date_from <= '2023-06-20')
                   OR (date_from <= '2023-05-15' AND date_to > '2023-05-15')
            )
            """
            booked_rooms_count = select(Rooms.hotel_id).select_from(Bookings).join(
                Rooms, Bookings.room_id == Rooms.id, isouter=True
            ).where(or_(
                and_(Bookings.date_from >= date_form, Bookings.date_from <= date_to),
                and_(Bookings.date_from <= date_form, Bookings.date_to > date_form))).cte('booked_rooms_count')

            """
            SELECT
                hotels.id,
                hotels.name,
                hotels.location,
                hotels.services,
                hotels.rooms_quantity,
                (hotels.rooms_quantity - COALESCE(COUNT(booked_rooms.hotel_id), 0))              
            FROM hotels
            LEFT JOIN booked_rooms ON hotels.id = booked_rooms.hotel_id
            WHERE hotels.location ILIKE '%Алтай%'
            GROUP BY hotels.id
            HAVING (hotels.rooms_quantity - COALESCE(COUNT(booked_rooms.hotel_id), 0)) > 0;
            """
            find_hotels = select(
                Hotels.id,
                Hotels.name,
                Hotels.location,
                Hotels.services,
                Hotels.rooms_quantity,
                (Hotels.rooms_quantity - coalesce(count(booked_rooms_count.c.hotel_id), 0)).label('rooms_left')
            ).select_from(
                Hotels
            ).join(
                booked_rooms_count,
                Hotels.id == booked_rooms_count.c.hotel_id,
                isouter=True,
            ).where(
                Hotels.location.ilike(f'%{location}%')
            ).group_by(
                Hotels.id
            ).having(
                Hotels.rooms_quantity - coalesce(count(booked_rooms_count.c.hotel_id), 0) > 0
            )

            found_hotels = await session.execute(find_hotels)
            found_hotels: list[dict] = found_hotels.mappings().all()
            # booked_rooms_count: int = booked_rooms.mappings().first().get('count')
            return found_hotels

