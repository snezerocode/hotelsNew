import pytest

from unittest import mock

# Добавление мока, который заменяет декоратор на пустую функцию, благодаря чему код не ломается
# функция в ковычках заменяется на лямбду - пустой декоратор. Месторасположение важно!
mock.patch("fastapi_cache.decorator.cache", lambda *args, **kwargs: lambda f: f).start()

import json

from src.api.dependencies import get_db
from src.config import settings
from src.database import Base, engine_null_pool, async_session_maker_null_pool
from src.models import *

from httpx import AsyncClient

from src.main import app
from src.schemas.hotels import HotelAdd
from src.schemas.rooms import RoomAdd
from src.utils.db_manager import DBManager


@pytest.fixture(scope="session", autouse=True)
async def check_test_engine():
    assert settings.MODE == "TEST"


@pytest.fixture
async def db() -> DBManager:
    async with DBManager(session_factory=async_session_maker_null_pool) as db:
        yield db


# генератор для тестовой бд
async def get_db_null_pool():
    async with DBManager(session_factory=async_session_maker_null_pool) as db:
        yield db


# переписывания метода получения генератора подключения к бд
app.dependency_overrides[get_db] = get_db_null_pool


# scope настройка прогона фикстуры function - перед каждой функцией,
# module - каждый файл, package - внутри папки, session - внутри сессии
@pytest.fixture(scope="session", autouse=True)
async def setup_database(check_test_engine):
    async with engine_null_pool.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    with open("tests/mocks/mock_hotels.json", "r", encoding="utf-8") as file_hotels:
        hotels_raw = json.load(file_hotels)

    with open("tests/mocks/mock_rooms.json", "r", encoding="utf-8") as file_rooms:
        rooms_raw = json.load(file_rooms)

    hotels_ = [HotelAdd.model_validate(hotel) for hotel in hotels_raw]
    rooms_ = [RoomAdd.model_validate(room) for room in rooms_raw]

    async with DBManager(session_factory=async_session_maker_null_pool) as db_:
        await db_.hotels.add_bulk(hotels_)
        await db_.rooms.add_bulk(rooms_)
        await db_.commit()


@pytest.fixture(scope="session")
async def ac() -> AsyncClient:
    async with AsyncClient(app=app, base_url="https://testserver") as ac:
        yield ac


@pytest.fixture(scope="session", autouse=True)
async def register_user(setup_database, ac):
    await ac.post(
        "/auth/register",
        json={
            "email": "email@example.com",
            "password": "123456"
        }
    )


@pytest.fixture(scope="session")
async def authenticated_ac(register_user, ac):
    resp = await ac.post(
        "/auth/login",
        json={
            "email": "email@example.com",
            "password": "123456",
        }
    )
    assert ac.cookies["access_token"]
    yield ac

# @pytest.fixture(scope="session" ,autouse=True)
# async def create_hotels(setup_database):
#     with open("tests/mocks/mock_hotels.json", "r", encoding="utf-8") as file:
#         hotels_json = json.load(file)
#         for data in hotels_json:
#             new_hotel_data = HotelAdd(title=data["title"], location=data["location"])
#             async with DBManager(session_factory=async_session_maker_null_pool) as db:
#                 await db.hotels.add(new_hotel_data)
#                 await db.commit()
#
# @pytest.fixture(scope="session" ,autouse=True)
# async def create_rooms(create_hotels):
#     with open("tests/mocks/mock_rooms.json", "r", encoding="utf-8") as file:
#         rooms_json = json.load(file)
#         for data in rooms_json:
#             new_room_data = RoomAdd(
#                 hotel_id=data["hotel_id"],
#                 description=data["description"],
#                 title=data["title"],
#                 price=data["price"],
#                 quantity=data["quantity"],
#             )
#             async with DBManager(session_factory=async_session_maker_null_pool) as db:
#                 await db.rooms.add(new_room_data)
#                 await db.commit()
