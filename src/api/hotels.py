from fastapi import APIRouter, Query, Body
from src.schemas.hotels import Hotel, HotelPatch
from dependencies import PaginationDep

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
def add_hotel(hotel_data: Hotel = Body(openapi_examples={
    "a": {"summary": "Sochi", "value": {
        "title": "Отель сочи 5 звезд у моря",
        "name": "otel_sochi_5_zverd"
    }},"b": {"summary": "Omsk", "value": {
        "title": "Отель Омска из Омска",
        "name": "otel_omsk_iz_omsk"
    }}
})):
    global hotels
    hotels.append(
        {
            "id": hotels[-1]["id"] + 1,
            "title": hotel_data.title,
            "name": hotel_data.name,
        }
    )
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
        return hotels_[(pagination.page - 1 ) * pagination.per_page : pagination.page * pagination.per_page ]
    else:
        return hotels_
