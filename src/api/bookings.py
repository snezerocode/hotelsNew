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



@router.post("/")
async def create_bookings(booking_data: BookingAddRequest, user_id: UserIdDep, db: DBDep):
    room = await db.rooms.get_one_or_none(id=booking_data.room_id)
    _booking_data = BookingAdd(user_id=user_id, price=room.price, **booking_data.model_dump())
    await db.bookings.add(_booking_data)
    await db.commit()

    return {"status":"ok", "data": _booking_data}




