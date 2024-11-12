from fastapi import APIRouter, Body
from src.api.dependencies import DBDep
from fastapi_cache.decorator import cache


from src.schemas.facilities import FacilityAdd
from src.tasks.tasks import test_task

router = APIRouter(prefix="/facilities", tags=["Удобства"])



@router.get("/")
@cache(expire=10)
async def get_facilities(db: DBDep):
    print("Getting from DB")
    result = await db.facilities.get_all()

    return {"status": "ok", "data": result}

@router.post("/")
async def create_facility(db: DBDep, facility_data: FacilityAdd = Body()):
    facility = await db.facilities.add(facility_data)
    await db.commit()

    test_task.delay()

    return {"status": "ok", "data": facility}




#from src.init import redis_manager
# @router.get("/")
# async def get_facilities(db: DBDep):
#     facilities_from_cache = await redis_manager.get("facilities")
#     if not facilities_from_cache:
#         print("Иду в Базу Данных")
#         facilities = result = await db.facilities.get_all()
#         facilities_schemas: list[dict] = [f.model_dump() for f in facilities]
#         facilities_json = json.dumps(facilities_schemas)
#         await redis_manager.set(facilities, facilities_json, 10)
#
#         return {"status": "ok", "data": facilities}
#     else:
#         facilities_dicts = json.loads(facilities_from_cache)
#         return {"status": "ok", "data": facilities_dicts}
