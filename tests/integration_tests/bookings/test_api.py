

async def test_add_booking(db, authenticated_ac):
    room_id = (await db.rooms.get_all())[0].id
    date_from = "2024-08-01"
    date_to = "2024-08-10"
    response = await authenticated_ac.post(
        "/bookings",
        json={
            "room_id": room_id,
            "date_from": date_from,
            "date_to": date_to,
        }
    )
    assert response
    assert response.status_code == 200
    res = response.json()
    assert res["status"] == "OK"
    assert  isinstance(res, dict)
    assert "data" in res
