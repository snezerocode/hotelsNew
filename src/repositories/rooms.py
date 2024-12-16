from datetime import date

from sqlalchemy import select, insert
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import joinedload

from src.exceptions import (
    DateToBeforeDateFromException,
    ObjectNotFoundException,
    RoomNotFoundException,
)
from src.models.rooms import RoomsOrm
from src.repositories.base import BaseRepository
from src.repositories.mappers.mappers import RoomDataMapper, RoomDataWithRelsDataMapper

from src.repositories.utils import rooms_ids_for_booking
from src.schemas.hotels import Hotel
from src.schemas.rooms import RoomAdd


class RoomsRepository(BaseRepository):
    model = RoomsOrm
    mapper = RoomDataMapper

    async def add(self, data: RoomAdd):
        # Проверка существования отеля
        hotel = await self.session.execute(
            select(Hotel).where(Hotel.id == data.hotel_id)
        )
        if not hotel.scalars().first():
            raise ObjectNotFoundException

        add_data_stmt = (
            insert(self.model).values(**data.model_dump()).returning(self.model)
        )
        result = await self.session.execute(add_data_stmt)
        model = result.scalars().one()
        return self.mapper.map_to_domain_entity(model)

    async def get_filtered_by_time(
        self,
        hotel_id,
        date_from: date,
        date_to: date,
    ):
        if date_to <= date_from:
            raise DateToBeforeDateFromException
        rooms_ids_to_get = rooms_ids_for_booking(date_from, date_to, hotel_id)

        query = (
            select(self.model)
            .options(joinedload(self.model.facilities))
            .filter(RoomsOrm.id.in_(rooms_ids_to_get))
        )
        result = await self.session.execute(query)
        return [
            RoomDataWithRelsDataMapper.map_to_domain_entity(model)
            for model in result.unique().scalars().all()
        ]

    async def get_one(self, **filter_by):
        # Основной запрос, сразу загружаем `facilities` через `joinedload`
        room_query = (
            select(self.model)
            .options(joinedload(self.model.facilities))
            .filter_by(**filter_by)
        )

        # Выполнение запроса и получение результата
        result = await self.session.execute(room_query)

        try:
            model = result.unique().scalar_one()
        except NoResultFound:
            raise RoomNotFoundException

        # Валидация полученной модели через Pydantic-схему с удобствами
        return RoomDataWithRelsDataMapper.map_to_domain_entity(model)
