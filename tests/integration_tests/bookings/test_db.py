from src.schemas.bookings import BookingAdd, BookingUpdate
from datetime import date


async def test_add_booking(db):
    user_id = (await db.users.get_all())[0].id
    room_id = (await db.rooms.get_all())[0].id
    booking_data = BookingAdd(
        room_id=room_id,
        user_id=user_id,
        date_from= date(year=2023, month=8, day=10),
        date_to= date(year=2024, month=8, day=20),

        price = 100,
    )
    await db.bookings.add(booking_data)

    booking = (await db.bookings.get_all())[0]

    # получить эту бронь и убедиться что она есть
    assert booking is not None
    print(type(booking))
    # обновить бронь

    data = BookingUpdate(
        date_from = date(year=2023, month=8, day=11),
        date_to = date(year=2024, month=8, day=22),
        price = 1000,
    )
    await db.bookings.edit(
        data,
        id= booking.id,

    )

    assert (await db.bookings.get_all())[0].price == 1000

    # удалить бронь
    await db.bookings.delete(id=booking.id)
    deleted_booking_from_db = await db.bookings.get_all()
    assert len(deleted_booking_from_db) == 0

    await db.commit()