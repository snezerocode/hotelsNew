from sqlalchemy import select, func
from datetime import date

from src.models import RoomsOrm, BookingsOrm
from src.models.bookings import BookingsOrm
from src.repositories.base import BaseRepository
from src.repositories.mappers.mappers import BookingDataMapper
from src.repositories.utils import rooms_ids_for_booking
from src.schemas.bookings import BookingAdd


class BookingsRepository(BaseRepository):
    model = BookingsOrm
    mapper = BookingDataMapper

    async def add_booking(self, data: BookingAdd, user_id: int):
        available_rooms_query = rooms_ids_for_booking(
            date_from=data.date_from,
            date_to=data.date_to,
        )
        #print(available_rooms_query)
        available_room_ids_result = await self.session.execute(available_rooms_query)
        #print(available_room_ids_result)
        available_room_ids = {row[0] for row in available_room_ids_result.fetchall()}
        print(available_room_ids)
        # Проверка доступности комнаты
        if data.room_id not in available_room_ids:
            raise ValueError("Комната уже забронирована или недоступна на указанный период.")

        # Получение данных о комнате
        room_query = select(RoomsOrm).filter_by(id=data.room_id)
        room_result = await self.session.execute(room_query)
        room = room_result.scalars().first()
        if not room:
            raise ValueError("Комната с указанным ID не найдена.")

        # # Создание запроса для получения существующих бронирований
        # existing_bookings_query = (
        #     select(func.count(BookingsOrm.id))
        #     .filter(
        #         BookingsOrm.room_id == data.room_id,
        #         BookingsOrm.date_from <= data.date_to,
        #         BookingsOrm.date_to >= data.date_from
        #     )
        # )
        # existing_bookings_result = await self.session.execute(existing_bookings_query)
        # existing_bookings_count = existing_bookings_result.scalar() or 0
        # print(existing_bookings_count)
        # print("room-id",data.room_id)
        # print("date_to",data.date_to)
        # print("date_from",data.date_from)
        # print("BookingsOrm.date_from", BookingsOrm.date_from)
        # print("BookingsOrm.date_to", BookingsOrm.date_to)
        # print(type(existing_bookings_count))
        #
        # # Проверка на превышение допустимого количества бронирований
        # if existing_bookings_count >= room.quantity:
        #     raise ValueError("Превышено максимальное количество бронирований для этой комнаты.")

        # Создание объекта SQLAlchemy
        booking = BookingsOrm(
            user_id=user_id,
            price=room.price,
            **data.model_dump()
        )

        # Добавление в базу данных
        self.session.add(booking)
        await self.session.commit()




