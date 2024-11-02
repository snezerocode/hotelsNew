from http.client import HTTPException
from fastapi import APIRouter, Body, HTTPException
from src.schemas.rooms import RoomAdd, RoomPatch, RoomAddRequest, RoomPatchRequest
from src.api.dependencies import DBDep

router = APIRouter(prefix="/hotels", tags=["Номера"])


@router.post("/{hotel_id}/rooms", summary="Добавление номера с передачей ID отеля")
async def create_room(hotel_id: int, db: DBDep, room_data: RoomAddRequest = Body(openapi_examples={
    "1": {"summary": "Standart double", "value": {
        "title": "Стандартный двухместный",
        "description": "Двухместынй номер",
        "price": 3000,
        "quantity": 3
    }}, "2": {"summary": "Standart single", "value": {
        "title": "Стандартный одноместный",
        "description": "Одноместный номер",
        "price": 2500,
        "quantity": 2
    }}
})):
    _room_data = RoomAdd(hotel_id=hotel_id, **room_data.model_dump())
    room = await db.rooms.add(_room_data)
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


@router.get("/{hotel_id}/rooms", summary="Получение всех номеров отеля")
async def get_rooms(hotel_id: int, db: DBDep):
    rooms = await db.rooms.get_filtered(hotel_id=hotel_id)

    return {"status": "OK", "data": rooms}
