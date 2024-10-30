from pydantic import BaseModel, Field


class HotelAdd(BaseModel):
    title: str
    location: str

    model_config = {
        "from_attributes": True
    }

class Hotel(HotelAdd):
    id: int

class HotelPatch(BaseModel):
    title: str | None = Field(None)
    location: str | None = Field(None)
