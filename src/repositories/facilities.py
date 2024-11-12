from src.models.facilities import FacilitiesOrm, RoomsFacilitiesOrm
from src.repositories.base import BaseRepository
from src.repositories.mappers.mappers import FacilityDataMapper
from src.schemas.facilities import Facility, RoomFacility
from sqlalchemy import select, delete, insert


class FacilitiesRepository(BaseRepository):
    model = FacilitiesOrm
    mapper = FacilityDataMapper

class RoomsFacilitiesRepository(BaseRepository):
    model = RoomsFacilitiesOrm
    schema = RoomFacility

    async def update_facilities(self, room_id: int, facilities_ids: list[int]) -> None:
        # Получаем id текущих удобств для данной комнаты
        current_facilities_query = select(RoomsFacilitiesOrm.facility_id).filter_by(room_id=room_id)
        current_facilities_result = await self.session.execute(current_facilities_query)
        current_facilities_ids: list[int] = current_facilities_result.scalars().all()

        # Определяем ids для удаления
        ids_to_delete: list[int] = list(set(current_facilities_ids) - set(facilities_ids))

        # Определяем ids для добавления
        ids_to_insert: list[int] = list(set(facilities_ids) - set(current_facilities_ids))

        # Удаляем старые удобства
        if ids_to_delete:
            delete_m2m_facilities_stmt = (
                delete(RoomsFacilitiesOrm)
                .filter(RoomsFacilitiesOrm.room_id == room_id,
                        RoomsFacilitiesOrm.facility_id.in_(ids_to_delete))

            )
            await self.session.execute(delete_m2m_facilities_stmt)


        # Добавляем новые удобства
        if ids_to_insert:
            insert_m2m_facilities_stmt = (
                insert(RoomsFacilitiesOrm)
                .values([{"room_id": room_id, "facility_id": f_id} for f_id in ids_to_insert])

            )
            await self.session.execute(insert_m2m_facilities_stmt)


