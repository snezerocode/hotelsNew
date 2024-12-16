from datetime import date
from fastapi import HTTPException


class CustomHTTPException(HTTPException):
    status_code = 500
    detail = None

    def __init__(self):
        super().__init__(status_code=self.status_code, detail=self.detail)


class CustomException(Exception):
    detail = "Какая то ошибка"

    def __init__(self, *args, **kwargs):
        super().__init__(self.detail, *args, **kwargs)


class ObjectNotFoundException(CustomException):
    detail = "Объект не найден"


class RoomNotFoundException(ObjectNotFoundException):
    detail = "Номер не найден"


class HotelNotFoundException(ObjectNotFoundException):
    detail = "Отель не найден"


class ObjectAlreadyExistsException(CustomException):
    detail = "Похожий объект уже существует"


class AllRoomsAreBookedException(CustomException):
    detail = "Все номера забронированы"


class DateToBeforeDateFromException(CustomException):
    detail = "Дата выезда раньше даты заезда"


class UserNotFoundException(CustomException):
    detail = "Пользователь не найден"


class WrongPasswordException(CustomException):
    detail = "Неверный пароль"


class UserNotFoundHTTPException(CustomHTTPException):
    status_code = 404
    detail = "Пользователь не найден"


class WrongPasswordHTTPException(CustomHTTPException):
    status_code = 409
    detail = "Неверный пароль"


class HotelNotFoundHTTPException(CustomHTTPException):
    status_code = 404
    detail = "Отеля с таким ID не найдено"


class RoomNotFoundHTTPException(CustomHTTPException):
    status_code = 404
    detail = "Номера с таким ID не найдено"


class UserAlreadyExistsHTTPException(CustomHTTPException):
    status_code = 409
    detail = "Пользовательл с таким email уже существует"


def check_date_to_after_date_from(date_from: date, date_to: date) -> None:
    if date_to <= date_from:
        raise HTTPException(
            status_code=400, detail="Дата заезда не может быть позже даты выезда"
        )
