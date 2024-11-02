from fastapi import APIRouter
from src.api.dependencies import UserIdDep
from src.api.dependencies import DBDep

from src.schemas.bookings import BookingAddRequest, BookingAdd

router = APIRouter(prefix="/bookings", tags=["Бронирования"])

@router.post("/")
async def create_bookings(booking_data: BookingAddRequest, user_id: UserIdDep, db: DBDep):
    room = await db.rooms.get_one_or_none(id=booking_data.room_id)
    _booking_data = BookingAdd(user_id=user_id, price=room.price, **booking_data.model_dump())
    await db.bookings.add(_booking_data)
    await db.commit()

    return {"status":"ok", "data": _booking_data}



