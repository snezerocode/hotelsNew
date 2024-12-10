from pydantic import BaseModel, ConfigDict
from datetime import date


class BookingAddRequest(BaseModel):
    room_id: int
    date_to: date
    date_from: date


class BookingAdd(BookingAddRequest):
    user_id: int
    price: int


class Booking(BookingAdd):
    id: int
    model_config = ConfigDict(from_attributes=True)


class BookingUpdate(BaseModel):
    date_from: date | None = None
    date_to: date | None = None
    price: int | None = None
