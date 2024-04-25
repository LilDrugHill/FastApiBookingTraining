from datetime import date

from fastapi import APIRouter, Request, Depends, Response
from sqlalchemy import select

from app.booking.dao import BookingDAO
from app.booking.models import Bookings
from app.booking.schemas import SBooking
from app.database import async_session_maker
from app.exceptions import RoomCannotBeBookedException, BookingDoesntExistsException, UserCannotDeleteBooking
from app.users.dependencies import get_current_user
from app.users.models import Users

router = APIRouter(
    prefix='/bookings',
    tags=['Бронирование'],
)


@router.get('')
async def get_bookings(user: Users = Depends(get_current_user)): # -> list[SBooking]:
    # async with async_session_maker() as session:
    #     query = select(Bookings) # SELECT * FROM bookings;
    #     result = await session.execute(query)
    #     # return result.scalars().all() # Конвертирует в json
    #     return result.mappings().all() # Тоже самое но без странностей
    # print(request.cookies)
    # print(request.url)
    # print(request.client)
    return await BookingDAO.find_all(user_id=user.id)


@router.post('/add')
async def add_booking(room_id: int, date_from: date, date_to: date, user: Users = Depends(get_current_user)):
    booking = await BookingDAO.add(user.id, room_id, date_from, date_to)
    if not booking:
        raise RoomCannotBeBookedException
    return booking


@router.delete('/{booking_id}', status_code=204)
async def delete_booking(booking_id: int, user: Users = Depends(get_current_user)):
    booking = await BookingDAO.find_one_or_none(id=booking_id)
    if not booking:
        raise BookingDoesntExistsException

    if not booking.user_id == user.id:
        raise UserCannotDeleteBooking

    await BookingDAO.delete(booking.id)

    return {'detail': 'Удалено'}


