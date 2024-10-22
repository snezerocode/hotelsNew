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
    global hotels
    for hotel in hotels:
        if hotel["id"] == id:
            if hotel_data.title:
                hotel["title"] = hotel_data.title
            if hotel_data.name:
                hotel["name"] = hotel_data.name
            return {"status": "ok"}
    return {"status": "not found"}


@router.delete("/{hotel_id}", summary="Удаление отеля по ID")
def delete_hotel(hotel_id: int):
    global hotels
    hotels = [hotel for hotel in hotels if hotel["id"] != hotel_id]
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
        await BaseRepository(session).add(hotel_data)
    return {"status": "ok", "data": hotel_data}


@router.put("/{hotel_id}", summary="Полное изменение свойств отеля", description="Все поля обязательны")
def edit_hotel(id: int, hotel_data: Hotel):
    global hotels
    for hotel in hotels:
        if hotel["id"] == id:
            hotel["title"] = hotel_data.title
            hotel["name"] = hotel_data.name
    return {"status": "ok"}


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
