from datetime import date

from fastapi import APIRouter

from app.exceptions import HotelDoesntExistsException
from app.hotels.dao import HotelsDAO
from app.hotels.rooms.schemas import SRoom

router = APIRouter()


@router.get('/{hotel_id}/rooms', response_model=list[SRoom])
async def get_rooms(hotel_id: int, date_from: date, date_to: date):
    hotel = await HotelsDAO.find_by_id(hotel_id)
    if not hotel:
        raise HotelDoesntExistsException
    return await HotelsDAO.get_hotel_rooms(hotel.id, date_from, date_to)
