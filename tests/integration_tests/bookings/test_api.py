import pytest

from src.models import BookingsOrm


@pytest.mark.parametrize("room_id, date_from, date_to, status_code", [
    (1, "2024-08-01", "2024-08-10", 200),
    (1, "2024-08-02", "2024-08-11", 200),
    (1, "2024-08-03", "2024-08-12", 200),
    (1, "2024-08-04", "2024-08-13", 200),
    (1, "2024-08-05", "2024-08-14", 200),
    (1, "2024-08-06", "2024-08-15", 500),
    (1, "2024-08-17", "2024-08-25", 200),
])
async def test_add_booking(
        room_id,
        date_from,
        date_to,
        status_code,
        db,
        authenticated_ac):
    # room_id = (await db.rooms.get_all())[0].id
    response = await authenticated_ac.post(
        "/bookings",
        json={
            "room_id": room_id,
            "date_from": date_from,
            "date_to": date_to,
        }
    )
    assert response
    assert response.status_code == status_code
    if status_code == 200:
        res = response.json()
        assert res["status"] == "OK"
        assert isinstance(res, dict)
        assert "data" in res


@pytest.fixture
async def delete_all_bookings(db):
    await db.bookings.delete()
    await db.commit()


@pytest.mark.parametrize("room_id, date_from, date_to, bookings_to_create", [
    (1, "2024-08-01", "2024-08-10", 1),
    (1, "2024-08-11", "2024-08-12", 2),
    (1, "2024-08-13", "2024-08-14", 3),
])
async def test_add_and_get_my_bookings(
        delete_all_bookings,
        authenticated_ac,
        room_id,
        date_from,
        date_to,
        bookings_to_create,
):
    # Создание указанного количества бронирований
    for _ in range(bookings_to_create):
        booking = await authenticated_ac.post(
            "/bookings",
            json={
                "room_id": room_id,
                "date_from": date_from,
                "date_to": date_to,
            }
        )
        assert booking.status_code == 200

    # Получение списка бронирований
    res_bookings = await authenticated_ac.get("/bookings/me")
    assert res_bookings.status_code == 200

    # Извлечение данных из ответа
    response_data = res_bookings.json()
    bookings_data = response_data["data"]
    bookings = [BookingsOrm(**item) for item in bookings_data if isinstance(item, dict)]

    # Проверка количества бронирований
    assert len(bookings) == bookings_to_create, f"Ожидалось {bookings_to_create} бронирований, но получено {len(bookings)}"

