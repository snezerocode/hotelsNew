from select import select

from fastapi import APIRouter, Query, Body

from src.database import async_session_maker
from src.models.hotels import HotelsOrm
from src.repositories.base import BaseRepository
from src.repositories.hotels import HotelsRepository
from src.schemas.hotels import Hotel, HotelPatch
from src.api.dependencies import PaginationDep

from sqlalchemy import insert, select, func
from src.database import engine

router = APIRouter(prefix="/hotel", tags=["Отели"])

hotels = [
    {"id": 1, "title": "Sochi", "name": "sochi"},
    {"id": 2, "title": "Dubai", "name": "dubai"},
    {"id": 3, "title": "Maldives", "name": "maldives"},
    {"id": 4, "title": "Gelenjik", "name": "gelenjik"},
    {"id": 5, "title": "Moscow", "name": "moscow"},
    {"id": 6, "title": "Kazan", "name": "kazan"},
    {"id": 7, "title": "SpB", "name": "spb"},

]


@router.patch("/{id}", summary="Частичное обновление данных об отеле", description="Длинное описание ")
def edit_hotel_attr(id: int, hotel_data: HotelPatch):

    with async_session_maker as session:
        HotelsRepository(session).edit(hotel_data, exclude_unset=True, id=id)
        session.commit()

    return {"status": "ok"}



@router.delete("/{hotel_id}", summary="Удаление отеля по ID")
async def delete_hotel(hotel_id: int):
    async with async_session_maker() as session:
        await HotelsRepository(session).delete(id=hotel_id)
        await session.commit()
    return {"status": "ok"}


@router.post("", summary="Добавление отеля")
async def add_hotel(hotel_data: Hotel = Body(openapi_examples={
    "a": {"summary": "Sochi", "value": {
        "title": "Отель сочи 5 звезд у моря",
        "location": "ул.Морская,  д2"
    }}, "b": {"summary": "Omsk", "value": {
        "title": "Отель Омска из Омска",
        "location": "ул. Шейха, д3"
    }}
})):
    async with async_session_maker() as session:
        hotel = await HotelsRepository(session).add(hotel_data)
        await session.commit()
    return {"status": "ok", "data": hotel}


@router.put("/{hotel_id}", summary="Полное изменение свойств отеля", description="Все поля обязательны")
async def edit_hotel(hotel_data: Hotel, id: int):
    async with async_session_maker() as session:
        await HotelsRepository(session).edit(hotel_data, id=id)
        await session.commit()
    return {"status": "ok"}

@router.get("/{hotel_id}", summary="Получение отеля по ID")
async def get_hotel(id: int):
    async with async_session_maker() as session:
        return await HotelsRepository(session).get_one_or_none(id=id)


@router.get("", summary="Получение списка отелей")
async def get_hotels(

        pagination: PaginationDep,
        location: str | None = Query(None, description="Адрес отеля"),
        title: str | None = Query(None, description="Название отеля"),

):
    per_page = pagination.per_page or 5
    async with async_session_maker() as session:
        return await HotelsRepository(session).get_all(
            location=location,
            title=title,
            limit=pagination.per_page or 5,
            offset=per_page * (pagination.page - 1)
        )
