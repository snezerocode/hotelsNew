from fastapi import APIRouter, Body, HTTPException, Query

from datetime import date

from src.exceptions import DateToBeforeDateFromException, ObjectNotFoundException
from src.schemas.facilities import RoomFacilityAdd
from src.schemas.rooms import RoomAdd, RoomPatch, RoomAddRequest, RoomPatchRequest
from src.api.dependencies import DBDep

router = APIRouter(prefix="/hotels", tags=["Номера"])


@router.get("/{hotel_id}/rooms/{room_id}", summary="Получение комнаты по ID")
async def get_room(hotel_id: int, room_id: int, db: DBDep):
    try:
        room = await db.rooms.get_one(id=room_id, hotel_id=hotel_id)
    except ObjectNotFoundException:
        raise HTTPException(status_code=404, detail="Отеля с таким ID не найдено")

    return {"status": "OK", "room": room}


@router.get("/{hotel_id}/rooms", summary="Получение всех номеров отеля")
async def get_rooms(
    hotel_id: int,
    db: DBDep,
    date_from: date = Query(example="2024-08-01"),
    date_to: date = Query(example="2024-08-10"),
):
    try:
        rooms = await db.rooms.get_filtered_by_time(
            hotel_id=hotel_id, date_from=date_from, date_to=date_to
        )
    except DateToBeforeDateFromException:
        raise HTTPException(status_code=400, detail="Дата выезда раньше даты заезда")

    return {"status": "OK", "data": rooms}


@router.post("/{hotel_id}/rooms", summary="Добавление номера с передачей ID отеля")
async def create_room(hotel_id: int, db: DBDep, room_data: RoomAddRequest = Body()):
    _room_data = RoomAdd(hotel_id=hotel_id, **room_data.model_dump())
    try:
        room = await db.rooms.add(_room_data)
    except ObjectNotFoundException:
        raise HTTPException(status_code=404, detail="Отеля с таким ID не найдено")

    rooms_facilities_data = [
        RoomFacilityAdd(room_id=room_data.id, facility_id=f_id)
        for f_id in room_data.facilities_ids
    ]
    print(rooms_facilities_data)
    await db.rooms_facilities.add_bulk(rooms_facilities_data)
    await db.commit()

    return {"status": "OK", "data": room}


@router.delete("/{hotel_id}/rooms/{room_id}", summary="Удаление номера по ID")
async def delete_room(hotel_id: int, db: DBDep, room_id: int):
    try:
        await db.rooms.get_one(id=room_id, hotel_id=hotel_id)
    except ObjectNotFoundException:
        raise HTTPException(status_code=404, detail="Комнаты с таким ID нет")
    await db.rooms.delete(id=room_id)
    await db.commit()

    return {"status": "OK"}


@router.put("/{hotel_id}/rooms/{room_id}/", summary="Полное обновление данных номера")
async def edit_room(hotel_id: int, db: DBDep, room_id: int, room_data: RoomAddRequest):
    _room_data = RoomAdd(hotel_id=hotel_id, **room_data.model_dump())
    try:
        await db.rooms.get_one(id=room_id, hotel_id=hotel_id)
    except ObjectNotFoundException:
        raise HTTPException(status_code=404, detail="Комнаты с таким ID нет")
    await db.rooms.edit(_room_data, id=room_id)

    await db.rooms_facilities.update_facilities(
        room_id=room_id, facilities_ids=room_data.facilities_ids
    )

    await db.commit()

    return {
        "status": "ok",
    }


@router.patch(
    "/{hotel_id}/rooms/{room_id}", summary="Частичное обновление данных о номере"
)
async def edit_room_attr(
    room_data: RoomPatchRequest, hotel_id: int, room_id: int, db: DBDep
):
    _room_data_dict = room_data.model_dump(exclude_unset=True)
    _room_data = RoomPatch(hotel_id=hotel_id, **_room_data_dict)

    try:
        await db.rooms.get_one(id=room_id, hotel_id=hotel_id)
    except ObjectNotFoundException:
        raise HTTPException(status_code=404, detail="Комнаты с таким ID нет")

    await db.rooms.edit(_room_data, id=room_id, exclude_unset=True)
    if "facilities_ids" in _room_data_dict:
        await db.rooms_facilities.update_facilities(
            room_id=room_id, facilities_ids=_room_data_dict["facilities_ids"]
        )

    await db.commit()

    return {"status": "ok"}
