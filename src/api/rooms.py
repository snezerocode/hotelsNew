from fastapi import APIRouter, Body, Query

from datetime import date

from src.exceptions import (
    HotelNotFoundHTTPException,
    RoomNotFoundHTTPException,
    RoomNotFoundException,
    HotelNotFoundException,
)

from src.schemas.rooms import RoomAddRequest, RoomPatchRequest
from src.api.dependencies import DBDep
from src.services.rooms import RoomService

router = APIRouter(prefix="/hotels", tags=["Номера"])


@router.get("/{hotel_id}/rooms/{room_id}", summary="Получение комнаты по ID")
async def get_room(hotel_id: int, room_id: int, db: DBDep):
    try:
        room = await db.rooms.get_one_or_none(id=room_id, hotel_id=hotel_id)
    except RoomNotFoundException:
        raise RoomNotFoundException
    return {"status": "OK", "room": room}


@router.get("/{hotel_id}/rooms", summary="Получение всех номеров отеля")
async def get_rooms(
    hotel_id: int,
    db: DBDep,
    date_from: date = Query(example="2024-08-01"),
    date_to: date = Query(example="2024-08-10"),
):
    rooms = await RoomService(db).get_filtered_by_time(
        hotel_id=hotel_id, date_from=date_from, date_to=date_to
    )

    return {"status": "OK", "data": rooms}


@router.post("/{hotel_id}/rooms", summary="Добавление номера с передачей ID отеля")
async def create_room(hotel_id: int, db: DBDep, room_data: RoomAddRequest = Body()):
    try:
        room = await RoomService(db).create_room(hotel_id, room_data)
    except HotelNotFoundException:
        raise HotelNotFoundHTTPException
    return {"status": "OK", "data": room}


@router.put("/{hotel_id}/rooms/{room_id}/", summary="Полное обновление данных номера")
async def edit_room(hotel_id: int, db: DBDep, room_id: int, room_data: RoomAddRequest):
    try:
        await RoomService(db).edit_room(hotel_id, room_id, room_data)
    except RoomNotFoundException:
        raise RoomNotFoundHTTPException
    except HotelNotFoundException:
        raise HotelNotFoundHTTPException

    return {
        "status": "ok",
    }


@router.patch(
    "/{hotel_id}/rooms/{room_id}", summary="Частичное обновление данных о номере"
)
async def edit_room_attr(
    room_data: RoomPatchRequest, hotel_id: int, room_id: int, db: DBDep
):
    try:
        await RoomService(db).edit_room_attr(room_data, hotel_id, room_id)
    except RoomNotFoundException:
        raise RoomNotFoundHTTPException
    except HotelNotFoundException:
        raise HotelNotFoundHTTPException

    return {"status": "ok"}


@router.delete("/{hotel_id}/rooms/{room_id}", summary="Удаление номера по ID")
async def delete_room(hotel_id: int, db: DBDep, room_id: int):
    try:
        await RoomService(db).delete_room(hotel_id, room_id)
    except RoomNotFoundException:
        raise RoomNotFoundHTTPException
    except HotelNotFoundException:
        raise HotelNotFoundHTTPException

    return {"status": "OK"}
