from datetime import date

from sqlalchemy import select
from sqlalchemy.orm import joinedload
from src.models.rooms import RoomsOrm
from src.repositories.base import BaseRepository
from src.repositories.mappers.mappers import RoomDataMapper, RoomDataWithRelsDataMapper

from src.repositories.utils import rooms_ids_for_booking


class RoomsRepository(BaseRepository):
    model = RoomsOrm
    mapper = RoomDataMapper

    async def get_filtered_by_time(
        self,
        hotel_id,
        date_from: date,
        date_to: date,
    ):
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

    async def get_one_or_none(self, **filter_by):
        # Основной запрос, сразу загружаем `facilities` через `joinedload`
        room_query = (
            select(self.model)
            .options(joinedload(self.model.facilities))
            .filter_by(**filter_by)
        )

        # Выполнение запроса и получение результата
        result = await self.session.execute(room_query)
        model = result.unique().scalar_one_or_none()

        if model is None:
            return None

        # Валидация полученной модели через Pydantic-схему с удобствами
        return RoomDataWithRelsDataMapper.map_to_domain_entity(model)
