from http.client import HTTPException
from shutil import which

from fastapi import APIRouter, Body, HTTPException
from pydantic import with_config

from src.database import async_session_maker
from src.repositories.hotels import HotelsRepository
from src.repositories.rooms import RoomsRepository
from src.schemas.rooms import RoomAdd, RoomPatch

router = APIRouter(prefix="/hotels/rooms", tags=["Номера"])

@router.post("/add_room", summary="Добавление номера с передачей ID отеля")
async def add_room_to_hotel(room_data: RoomAdd = Body(openapi_examples={
    "1": {"summary": "Standart double", "value": {
        "hotel_id": 1,
        "title": "Стандартный двухместный",
        "description": "Двухместынй номер",
        "price": 3000,
        "quantity": 3
    }},"2": {"summary": "Standart single", "value": {
        "hotel_id": 5,
        "title": "Стандартный одноместный",
        "description": "Одноместный номер",
        "price": 2500,
        "quantity": 2
    }}
})):
    async with async_session_maker() as session:
        hotel = await HotelsRepository(session).get_one_or_none(id=room_data.hotel_id)
        if not hotel:
            raise HTTPException(status_code=404, detail="Отель не найден")
        await RoomsRepository(session).add(room_data)
        await session.commit()

    return {"status": "OK"}

@router.delete("/{id}", summary="Удаление номера по ID")
async def delete_room(id: int):
    async with async_session_maker() as session:
        room = await RoomsRepository(session).get_one_or_none(id=id)
        if not room:
            raise HTTPException(status_code=404, detail="Комнаты с таким ID нет")
        await RoomsRepository(session).delete(id=id)
        await session.commit()
    return {"status": "OK"}

@router.put("/{id}", summary="Полное обновление данных номера")
async def edit_room(room_data: RoomAdd, id: int):
    async with async_session_maker() as session:
        room = await RoomsRepository(session).get_one_or_none(id=id)
        if not room:
            raise HTTPException(status_code=404, detail="Комнаты с таким ID нет")
        await RoomsRepository(session).edit(room_data, id=id)
        await session.commit()

    return {"status:" "ok"}

@router.patch("/{id}", summary="Частичное обновление данных о номере")
async def edit_room_attr(room_data: RoomPatch, id:int):
    async with async_session_maker() as session:
        room = await RoomsRepository(session).get_one_or_none(id=id)
        if not room:
            raise HTTPException(status_code=404, detail="Комната не найдена")
        await RoomsRepository(session).edit(room_data, id=id)
        await session.commit()
    return {"status:" "ok"}

@router.get("/get_one/{id}", summary="Получение комнаты по ID")
async def get_one_room(room_id: int):
    async with async_session_maker() as session:
        room = await RoomsRepository(session).get_one_or_none(id=room_id)
        if not room:
            raise HTTPException(status_code=404, detail="Комната не найдена")
        return {"status": "OK", "room": room}

@router.get("/get_all", summary="Получение всех номеров отеля")
async def get_all_rooms():
    async with async_session_maker() as session:
        rooms = await RoomsRepository(session).get_all()
        return {"status": "OK", "data": rooms}