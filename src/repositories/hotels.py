from sqlalchemy import select, func

from src.models.hotels import HotelsOrm
from src.repositories.base import BaseRepository


class HotelsRepository(BaseRepository):
    model = HotelsOrm

    async def get_all(
            self,
            location,
            title,
            limit,
            offset
    ):

        query = select(HotelsOrm)
        if location:
            query = query.filter(func.lower(HotelsOrm.location).contains(location.strip().lower()))
        if title:
            query = query.filter(func.lower(HotelsOrm.title).contains(title.strip().lower()))
        query = (
            query
            .limit(limit)
            .offset(offset)
        )
        result = await self.session.execute(query)
        return result.scalars().all()

    async def get_one_or_none(self, id):
        query = select(HotelsOrm).filter_by(id=id)
        result = await self.session.execute(query)
        return result.scalars().one_or_none()