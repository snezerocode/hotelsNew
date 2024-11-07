from http.client import HTTPException
from fastapi import APIRouter, Body, HTTPException, Query

from datetime import date

from src.schemas.facilities import RoomFacilityAdd
from src.schemas.rooms import RoomAdd, RoomPatch, RoomAddRequest, RoomPatchRequest
from src.api.dependencies import DBDep

router = APIRouter(prefix="/hotels", tags=["Номера"])


@router.get("/{hotel_id}/rooms", summary="Получение всех номеров отеля")
async def get_rooms(
        hotel_id: int,
        db: DBDep,
        date_from: date = Query(example="2024-08-01"),
        date_to: date = Query(example="2024-08-10"),
):
    rooms = await db.rooms.get_filtered_by_time(hotel_id=hotel_id, date_from=date_from, date_to=date_to)

    return {"status": "OK", "data": rooms}


@router.post("/{hotel_id}/rooms", summary="Добавление номера с передачей ID отеля")
async def create_room(hotel_id: int, db: DBDep, room_data: RoomAddRequest = Body()):
    _room_data = RoomAdd(hotel_id=hotel_id, **room_data.model_dump())
    room = await db.rooms.add(_room_data)

    rooms_facilities_data = [RoomFacilityAdd(room_id=room.id, facility_id=f_id) for f_id in room_data.facilities_ids]
    print(rooms_facilities_data)
    await db.rooms_facilities.add_bulk(rooms_facilities_data)
    await db.commit()

    return {"status": "OK", "data": room}


@router.delete("/{hotel_id}/rooms/{room_id}", summary="Удаление номера по ID")
async def delete_room(hotel_id: int, db: DBDep, room_id: int):
    room = await db.rooms.get_one_or_none(id=room_id, hotel_id=hotel_id)
    if not room:
        raise HTTPException(status_code=404, detail="Комнаты с таким ID нет")
    await db.rooms.delete(id=room_id)
    await db.commit()

    return {"status": "OK"}


@router.put("/{hotel_id}/rooms/{room_id}", summary="Полное обновление данных номера")
async def edit_room(hotel_id: int, db: DBDep, room_id: int, room_data: RoomAddRequest):
    _room_data = RoomAdd(hotel_id=hotel_id, **room_data.model_dump())
    room = await db.rooms.get_one_or_none(id=room_id, hotel_id=hotel_id)
    if not room:
        raise HTTPException(status_code=404, detail="Комнаты с таким ID нет")



    await db.rooms.edit(_room_data, id=room_id)
    await db.commit()

    return {"status:" "ok"}


@router.patch("/{hotel_id}/rooms/{room_id}", summary="Частичное обновление данных о номере")
async def edit_room_attr(room_data: RoomPatchRequest, hotel_id: int, room_id: int, db: DBDep):
    _room_data = RoomPatch(hotel_id=hotel_id, **room_data.model_dump(exclude_unset=True))

    room = await db.rooms.get_one_or_none(id=room_id, hotel_id=hotel_id)
    if not room:
        raise HTTPException(status_code=404, detail="Комната не найдена")
    await db.rooms.edit(_room_data, id=room_id, exclude_unset=True)
    await db.commit()

    return {"status:" "ok"}


@router.get("/{hotel_id}/rooms/{room_id}", summary="Получение комнаты по ID")
async def get_room(hotel_id: int, room_id: int, db: DBDep):
    room = await db.rooms.get_one_or_none(id=room_id, hotel_id=hotel_id)
    if not room:
        raise HTTPException(status_code=404, detail="Комната не найдена")

    return {"status": "OK", "room": room}


