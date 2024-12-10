async def test_get_facilities(ac):
    response = await ac.get("/facilities")
    assert response.status_code == 200


async def test_add_facilities(ac, db):
    new_facility = {"title": "Spa"}
    added_facility = (await ac.post("/facilities", json=new_facility)).json()
    print(added_facility)
    facility = await db.facilities.get_one_or_none(id=added_facility["data"]["id"])

    assert facility.title == new_facility["title"]
