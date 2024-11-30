from fastapi import HTTPException

from fastapi import APIRouter
from src.api.dependencies import UserIdDep
from src.api.dependencies import DBDep

from src.schemas.bookings import BookingAddRequest, BookingAdd

router = APIRouter(prefix="/bookings", tags=["Бронирования"])

@router.get("")
async def get_all_bookings(db: DBDep):
    result = await db.bookings.get_all()
    return {"status":"ok", "data": result}

@router.get("/me")
async def get_user_bookings(user_id: UserIdDep, db: DBDep):

    user = await db.users.get_one_or_none(id=user_id)

    result = await db.bookings.get_filtered(user_id=user.id)
    return {"status": "ok", "data": result}



@router.post("")
async def add_booking(booking_data: BookingAddRequest, user_id: UserIdDep, db: DBDep):
    room = await db.rooms.get_one_or_none(id=booking_data.room_id)
    hotel = await db.hotels.get_one_or_none(id=room.hotel_id)
    room_price: int = room.price
    _booking_data = BookingAdd(
        user_id=user_id,
        price=room_price,
        **booking_data.model_dump(),
    )
    booking = await db.bookings.add_booking(_booking_data, hotel_id=hotel.id)
    await db.commit()
    return {"status": "OK", "data": booking}





