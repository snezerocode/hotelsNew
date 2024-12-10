from src.schemas.bookings import BookingAdd, BookingUpdate
from datetime import date


async def test_booking_crud(db):
    user_id = (await db.users.get_all())[0].id
    room_id = (await db.rooms.get_all())[0].id
    booking_data = BookingAdd(
        room_id=room_id,
        user_id=user_id,
        date_from=date(year=2023, month=8, day=10),
        date_to=date(year=2024, month=8, day=20),
        price=100,
    )
    new_booking = await db.bookings.add(booking_data)

    # получить эту бронь и убедиться что она есть
    booking = await db.bookings.get_one_or_none(id=new_booking.id)
    assert booking
    assert booking.id == new_booking.id
    assert booking.room_id == new_booking.room_id
    assert booking.user_id == new_booking.user_id
    # обновить бронь

    update_booking_data = BookingUpdate(
        date_from=date(year=2023, month=8, day=11),
        date_to=date(year=2024, month=8, day=22),
        price=1000,
    )
    await db.bookings.edit(
        update_booking_data,
        id=booking.id,
    )

    updated_booking = await db.bookings.get_one_or_none(id=booking.id)
    assert updated_booking
    assert updated_booking.id == booking.id
    assert updated_booking.price == 1000

    # удалить бронь
    await db.bookings.delete(id=booking.id)
    deleted_booking_from_db = await db.bookings.get_one_or_none(id=booking.id)
    assert not deleted_booking_from_db

    await db.commit()
