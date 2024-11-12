
import pytest
import json
from src.config import settings
from src.database import Base, engine_null_pool, async_session_maker_null_pool
from src.models import *

from httpx import AsyncClient

from src.main import app
from src.schemas.hotels import HotelAdd
from src.schemas.rooms import RoomAdd
from src.utils.db_manager import DBManager


@pytest.fixture(scope="session" ,autouse=True)
async def check_test_engine():
    assert settings.MODE == "TEST"


#scope настройка прогона фикстуры function - перед каждой функцией,
# module - каждый файл, package - внутри папки, session - внутри сессии
@pytest.fixture(scope="session" ,autouse=True)
async def setup_database(check_test_engine):

    async with engine_null_pool.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

@pytest.fixture(scope="session" ,autouse=True)
async def register_user(setup_database):
    async with AsyncClient(app=app, base_url="https://test") as ac:
        await ac.post(
            "/auth/register",
            json={
                "email": "email@example.com",
                "password": "123456"
            }
        )

@pytest.fixture(scope="session" ,autouse=True)
async def create_hotels(setup_database):
    with open("tests/mocks/mock_hotels.json", "r", encoding="utf-8") as file:
        hotels_json = json.load(file)
        for data in hotels_json:
            new_hotel_data = HotelAdd(title=data["title"], location=data["location"])
            async with DBManager(session_factory=async_session_maker_null_pool) as db:
                await db.hotels.add(new_hotel_data)
                await db.commit()

@pytest.fixture(scope="session" ,autouse=True)
async def create_rooms(create_hotels):
    with open("tests/mocks/mock_rooms.json", "r", encoding="utf-8") as file:
        rooms_json = json.load(file)
        for data in rooms_json:
            new_room_data = RoomAdd(
                hotel_id=data["hotel_id"],
                description=data["description"],
                title=data["title"],
                price=data["price"],
                quantity=data["quantity"],
            )
            async with DBManager(session_factory=async_session_maker_null_pool) as db:
                await db.rooms.add(new_room_data)
                await db.commit()