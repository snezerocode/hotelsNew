from pydantic import BaseModel, Field

class RoomAdd(BaseModel):
    hotel_id: int
    title: str
    description: str
    price: int
    quantity: int

class Room(RoomAdd):
    id: int

    model_config = {
        "from_attributes": True  # Включаем для поддержки ORM-атрибутов
    }

class RoomPatch(BaseModel):

    title: str | None = Field(None)
    description: str | None = Field(None)
    price: int | None = Field(None)
    quantity: int | None = Field(None)