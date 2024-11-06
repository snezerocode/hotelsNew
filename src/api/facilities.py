from fastapi import APIRouter
from src.api.dependencies import DBDep

from src.schemas.facilities import FacilityAddRequest

router = APIRouter(prefix="/facilities", tags=["Удобства"])

@router.get("/")
async def get_facilities(db: DBDep):
    result = await db.facilities.get_all()

    return {"status": "ok", "data": result}

@router.post("/")
async def create_facility(facility_data: FacilityAddRequest, db: DBDep):
    facility = await db.facilities.add(facility_data)
    await db.commit()

    return {"status": "ok", "data": facility}