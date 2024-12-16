from fastapi import APIRouter, Query, Body
from datetime import date


from src.exceptions import (
    ObjectNotFoundException,
    HotelNotFoundHTTPException,
)
from src.schemas.hotels import HotelPatch, HotelAdd
from src.api.dependencies import PaginationDep, DBDep
from fastapi_cache.decorator import cache

from src.services.hotels import HotelService

router = APIRouter(prefix="/hotels", tags=["Отели"])


@router.get("/{hotel_id}", summary="Получение отеля по ID")
async def get_hotel(hotel_id: int, db: DBDep):
    try:
        return await HotelService(db).get_hotel(hotel_id=hotel_id)
    except ObjectNotFoundException:
        raise HotelNotFoundHTTPException


@router.get("", summary="Получение списка отелей")
@cache(expire=100)
async def get_hotels(
    pagination: PaginationDep,
    db: DBDep,
    location: str | None = Query(None, description="Адрес отеля"),
    title: str | None = Query(None, description="Название отеля"),
    date_from: date = Query(example="2024-08-01"),
    date_to: date = Query(example="2024-08-10"),
):
    hotels = await HotelService(db).get_filtered_by_time(
        pagination,
        location,
        title,
        date_from,
        date_to,
    )
    return {"status": "OK", "data": hotels}


@router.post("", summary="Добавление отеля")
async def add_hotel(
    db: DBDep,
    hotel_data: HotelAdd = Body(
        openapi_examples={
            "a": {
                "summary": "Sochi",
                "value": {
                    "title": "Отель сочи 5 звезд у моря",
                    "location": "ул.Морская,  д2",
                },
            },
            "b": {
                "summary": "Omsk",
                "value": {"title": "Отель Омска из Омска", "location": "ул. Шейха, д3"},
            },
        }
    ),
):
    hotel = await HotelService(db).create_hotel(hotel_data)

    return {"status": "ok", "data": hotel}


@router.put(
    "/{hotel_id}",
    summary="Полное изменение свойств отеля",
    description="Все поля обязательны",
)
async def edit_hotel(hotel_data: HotelAdd, hotel_id: int, db: DBDep):
    await HotelService(db).edit_hotel(hotel_data, hotel_id)
    return {"status": "ok"}


@router.patch(
    "/{id}",
    summary="Частичное обновление данных об отеле",
    description="Длинное описание ",
)
async def edit_hotel_attr(hotel_id: int, hotel_data: HotelPatch, db: DBDep):
    await HotelService(db).edit_hotel_attr(hotel_id, hotel_data)

    return {"status": "ok"}


@router.delete("/{hotel_id}", summary="Удаление отеля по ID")
async def delete_hotel(hotel_id: int, db: DBDep):
    await HotelService(db).delete_hotel(hotel_id)

    return {"status": "ok"}
