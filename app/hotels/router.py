from datetime import date

from fastapi import APIRouter, Response

from app.hotels.dao import HotelsDAO
from app.hotels.schemas import SHotel, SHotelsByParam
from app.hotels.rooms.router import router as rooms_router

router = APIRouter(prefix="/hotels", tags=['Отели', ])


# class HotelSearchArgs:
#     def __init__(
#             self,
#             date_from: date,
#             date_to: date,
#             location: str,
#             stars: Optional[int] = Query(None, ge=1, le=5),
#             has_spa: Optional[bool] = None,
#     ):
#         self.date_from = date_from
#         self.date_to = date_to
#         self.location = location
#         self.stars = stars
#         self.has_spa = has_spa
#
#
# @router.get('', response_model=list[SHotel])
# def get_hotels(search_args: HotelSearchArgs = Depends()):
#     hotels = [
#         {
#             'address': 'sald, mas',
#             'name': 'Super hotel',
#             'stars': 5,
#         },
#     ]
#     return hotels

@router.get('', response_model=list[SHotel])
async def get_hotels():
    return await HotelsDAO.find_all()


@router.get('/id/{hotel_id}', response_model=SHotel)
async def get_hotel_info(hotel_id: int):
    return await HotelsDAO.find_by_id(hotel_id)


router.include_router(rooms_router)


# @router.get('/{hotel_id}/rooms')
# async def get_rooms(hotel_id: int):
#     hotel = await HotelsDAO.find_by_id(hotel_id)
#     if not hotel:
#         raise HotelDoesntExists
#     return await HotelsDAO.get_all_rooms(hotel.id)


@router.get('/{location}', response_model=list[SHotelsByParam])
async def get_hotels_with_param(response: Response, location: str, date_from: date, date_to: date):
    response.headers['Content-Type'] = 'application/json; charset=utf-8'     # Без этой строки рус
    return await HotelsDAO.get_hotel_by_param(location, date_from, date_to)  # текст в неверной кодировке
