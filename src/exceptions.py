
class CustomException(Exception):
    detail = "Какая то ошибка"

    def __init__(self, *args, **kwargs):
        super().__init__(self.detail, *args, **kwargs)



class ObjectNotFoundException(CustomException):
    detail = "Объект не найден"

class AllRoomsAreBookedException(CustomException):
    detail = "Все номера забронированы"

class DateToBeforeDateFromException(CustomException):
    detail = "Дата выезда раньше даты заезда"