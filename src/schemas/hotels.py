from pydantic import BaseModel, ConfigDict


class HotelAdd(BaseModel):
    title: str
    location: str

    model_config = {
        "from_attributes": True
    }

class Hotel(HotelAdd):
    id: int
    model_config = ConfigDict(from_attributes=True)

class HotelPatch(BaseModel):
    title: str | None = None
    location: str | None = None
