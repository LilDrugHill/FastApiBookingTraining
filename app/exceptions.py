from fastapi import HTTPException, status


class BookingException(HTTPException):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    detail = ''

    def __init__(self):
        super().__init__(status_code=self.status_code, detail=self.detail)


class UserAlreadyExistsException(BookingException):
    status_code = status.HTTP_409_CONFLICT
    detail = 'Пользователь уже существует'


class IncorrectEmailOrPasswordExecption(BookingException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = 'Неверная почта или пароль'


class TokenExpiredException(BookingException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = 'Токен истек'


class TokenAbsentException(BookingException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = 'Токен отсутствует. Попробуйте /register или /login'


class IncorrectTokenFormatException(BookingException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = 'Неверный формат токена'


class UserIsNotPresentException(BookingException):
    status_code = status.HTTP_401_UNAUTHORIZED


class RoomCannotBeBookedException(BookingException):
    status_code = status.HTTP_409_CONFLICT
    detail = 'Не осталось свободных номеров'


class HotelDoesntExistsException(BookingException):
    status_code = status.HTTP_404_NOT_FOUND
    detail = 'Отель не найден'


class BookingDoesntExistsException(BookingException):
    status_code = status.HTTP_404_NOT_FOUND
    detail = 'Бронирования не существует'


class UserCannotDeleteBooking(BookingException):
    status_code = status.HTTP_403_FORBIDDEN
    detail = 'Запрещено'



