from sqlalchemy import select

from fastapi import HTTPException

from datetime import date

from src.exceptions import AllRoomsAreBookedException, DateToBeforeDateFromException
from src.models.bookings import BookingsOrm
from src.repositories.base import BaseRepository
from src.repositories.mappers.mappers import BookingDataMapper
from src.repositories.utils import rooms_ids_for_booking
from src.schemas.bookings import BookingAdd


class BookingsRepository(BaseRepository):
    model = BookingsOrm
    mapper = BookingDataMapper

    async def add_booking(self, data: BookingAdd, hotel_id: int):
        if data.date_to <= data.date_from:
            raise DateToBeforeDateFromException
        rooms_ids_to_get = rooms_ids_for_booking(
            date_from=data.date_from, date_to=data.date_to, hotel_id=hotel_id
        )
        rooms_ids_to_book_res = await self.session.execute(rooms_ids_to_get)
        rooms_ids_to_book: list[int] = rooms_ids_to_book_res.scalars().all()

        if data.room_id in rooms_ids_to_book:
            new_booking = await self.add(data)
            return new_booking
        else:
            raise AllRoomsAreBookedException

    async def get_bookings_with_today_checkin(self):
        today = date.today()  # Получаем сегодняшнюю дату
        query = (
            select(BookingsOrm)  # Здесь указываем только модель
            .where(BookingsOrm.date_from == today)  # Фильтруем по дате
        )
        res = await self.session.execute(query)  # Добавляем await для асинхронного вызова
        return [self.mapper.map_to_domain_entity(booking) for booking in res.scalars().all()]