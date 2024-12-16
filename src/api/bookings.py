from fastapi import HTTPException

from fastapi import APIRouter
from src.api.dependencies import UserIdDep
from src.api.dependencies import DBDep
from src.exceptions import (
    ObjectNotFoundException,
    AllRoomsAreBookedException,
    DateToBeforeDateFromException,
)

from src.schemas.bookings import BookingAddRequest, BookingAdd
from src.schemas.hotels import Hotel
from src.schemas.rooms import Room

router = APIRouter(prefix="/bookings", tags=["Бронирования"])


@router.get("")
async def get_all_bookings(db: DBDep):
    result = await db.bookings.get_all()
    return {"status": "ok", "data": result}


@router.get("/me")
async def get_user_bookings(user_id: UserIdDep, db: DBDep):
    user = await db.users.get_one_or_none(id=user_id)

    result = await db.bookings.get_filtered(user_id=user.id)
    return {"status": "ok", "data": result}


@router.post("")
async def add_booking(booking_data: BookingAddRequest, user_id: UserIdDep, db: DBDep):
    try:
        room: Room | None = await db.rooms.get_one(id=booking_data.room_id)
    except ObjectNotFoundException:
        raise HTTPException(status_code=400, detail="Номер не найден")
    except DateToBeforeDateFromException:
        raise HTTPException(status_code=400, detail="Дата заезда позже даты выезда")
    # if not room:
    #     raise HTTPException(status_code=404, detail="Номер не найден")
    hotel: Hotel = await db.hotels.get_one(id=room.hotel_id)
    room_price: int = room.price
    _booking_data = BookingAdd(
        user_id=user_id,
        price=room_price,
        **booking_data.model_dump(),
    )
    try:
        booking = await db.bookings.add_booking(_booking_data, hotel_id=hotel.id)
    except AllRoomsAreBookedException:
        raise HTTPException(status_code=409, detail="Все номера забронированы")
    await db.commit()
    return {"status": "OK", "data": booking}
