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
async def create_bookings(booking_data: BookingAddRequest, user_id: UserIdDep, db: DBDep):
    try:
        # Передать данные в репозиторий для создания бронирования
        await db.bookings.add_booking(data=booking_data, user_id=user_id)
        return {"status": "OK", "message": "Бронирование успешно создано."}
    except ValueError as e:
        # Обработать ошибки, возникающие в репозитории
        raise HTTPException(status_code=400, detail=str(e))






