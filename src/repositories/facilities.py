from src.models.facilities import FacilitiesOrm, RoomsFacilitiesOrm
from src.repositories.base import BaseRepository
from src.schemas.facilities import Facility, RoomFacility
from sqlalchemy import select, delete


class FacilitiesRepository(BaseRepository):
    model = FacilitiesOrm
    schema = Facility

class RoomsFacilitiesRepository(BaseRepository):
    model = RoomsFacilitiesOrm
    schema = RoomFacility

    async def update_facilities(self, room_id: int, facilities_ids: list[int]):
        # Получаем текущие удобства для данной комнаты
        current_facilities_query = select(RoomsFacilitiesOrm).where(RoomsFacilitiesOrm.room_id == room_id)
        current_facilities_result = await self.session.execute(current_facilities_query)
        current_facilities = current_facilities_result.scalars().all()

        # Извлекаем ID текущих удобств
        current_facility_ids = {facility.facility_id for facility in current_facilities}

        # Определяем новые удобства для добавления
        new_facility_ids = set(facilities_ids)

        # Определяем удобства для удаления (которые есть в базе, но не переданы)
        facilities_to_remove = current_facility_ids - new_facility_ids

        # Удаляем старые удобства
        if facilities_to_remove:
            await self.session.execute(
                delete(RoomsFacilitiesOrm).where(
                    RoomsFacilitiesOrm.room_id == room_id,
                    RoomsFacilitiesOrm.facility_id.in_(facilities_to_remove)
                )
            )

        # Определяем удобства для добавления (которые переданы, но отсутствуют в базе)
        facilities_to_add = new_facility_ids - current_facility_ids

        # Добавляем новые удобства
        for facility_id in facilities_to_add:
            new_facility = RoomsFacilitiesOrm(room_id=room_id, facility_id=facility_id)
            self.session.add(new_facility)

        await self.session.commit()  # Фиксируем изменения в базе данных

        return {
            "removed_facilities": list(facilities_to_remove),
            "added_facilities": list(facilities_to_add)
        }  # Возвращаем ID удаленных и добавленных удобств
