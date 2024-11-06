from pydantic import BaseModel, ConfigDict


class FacilityAddRequest(BaseModel):
    title: str

class Facility(FacilityAddRequest):
    id: int

    model_config = ConfigDict(from_attributes=True)