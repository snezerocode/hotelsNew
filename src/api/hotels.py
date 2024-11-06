from fastapi import APIRouter, Query, Body
from datetime import date
from src.schemas.hotels import HotelPatch, HotelAdd
from src.api.dependencies import PaginationDep, DBDep

router = APIRouter(prefix="/hotel", tags=["Отели"])

@router.get("/{hotel_id}", summary="Получение отеля по ID")
async def get_hotel(hotel_id: int, db: DBDep):
    return await db.hotels.get_one_or_none(id=hotel_id)


@router.get("", summary="Получение списка отелей")
async def get_hotels(

        pagination: PaginationDep,
        db: DBDep,
        location: str | None = Query(None, description="Адрес отеля"),
        title: str | None = Query(None, description="Название отеля"),
        date_from: date = Query(example="2024-08-01"),
        date_to: date = Query(example="2024-08-10"),

):
    per_page = pagination.per_page or 5
    return await db.hotels.get_filtered_by_time(
        date_from=date_from,
        date_to=date_to,
        location=location,
        title=title,
        limit=per_page,
        offset=per_page * (pagination.page - 1)
    )




@router.post("", summary="Добавление отеля")
async def add_hotel(db: DBDep, hotel_data: HotelAdd = Body(openapi_examples={
    "a": {"summary": "Sochi", "value": {
        "title": "Отель сочи 5 звезд у моря",
        "location": "ул.Морская,  д2"
    }}, "b": {"summary": "Omsk", "value": {
        "title": "Отель Омска из Омска",
        "location": "ул. Шейха, д3"
    }}
})):
    hotel = await db.hotels.add(hotel_data)
    await db.commit()

    return {"status": "ok", "data": hotel}


@router.put("/{hotel_id}", summary="Полное изменение свойств отеля", description="Все поля обязательны")
async def edit_hotel(hotel_data: HotelAdd, hotel_id: int, db: DBDep):
    await db.hotels.edit(hotel_data, id=hotel_id)
    await db.commit()

    return {"status": "ok"}


@router.patch("/{id}", summary="Частичное обновление данных об отеле", description="Длинное описание ")
async def edit_hotel_attr(hotel_id: int, hotel_data: HotelPatch, db: DBDep):
    await db.hotels.edit(hotel_data, exclude_unset=True, id=hotel_id)
    await db.commit()

    return {"status": "ok"}


@router.delete("/{hotel_id}", summary="Удаление отеля по ID")
async def delete_hotel(hotel_id: int, db: DBDep):
    await db.hotels.delete(id=hotel_id)
    await db.commit()

    return {"status": "ok"}
