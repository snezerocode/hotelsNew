from fastapi import APIRouter, Query, Body
from sqlalchemy.util import await_only

from src.database import async_session_maker
from src.models.hotels import HotelsOrm
from src.schemas.hotels import Hotel, HotelPatch
from dependencies import PaginationDep

from sqlalchemy import insert

router = APIRouter(prefix="/hotelsBack", tags=["Отели"])

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
        add_hotel_stmt = insert(HotelsOrm).values(**hotel_data.model_dump())
        await session.execute(add_hotel_stmt)
        await session.commit()

    return {"status": "ok"}


@router.put("/{hotel_id}", summary="Полное изменение свойств отеля", description="Все поля обязательны")
def edit_hotel(id: int, hotel_data: Hotel):
    global hotels
    for hotel in hotels:
        if hotel["id"] == id:
            hotel["title"] = hotel_data.title
            hotel["name"] = hotel_data.name
    return {"status": "ok"}


@router.get("", summary="Получение списка отелей")
def get_hotels(
        pagination: PaginationDep,
        id: int | None = Query(None, description="Айдишник"),
        title: str | None = Query(None, description="Название отеля"),

):
    hotels_ = []
    for hotel in hotels:
        if hotel["id"] and id != id:
            continue
        if hotel["title"] and title != title:
            continue
        hotels_.append(hotel)
    if pagination.page and pagination.per_page:
        return hotels_[(pagination.page - 1) * pagination.per_page: pagination.page * pagination.per_page]
    else:
        return hotels_
