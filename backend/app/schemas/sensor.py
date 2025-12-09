from pydantic import BaseModel
from uuid import UUID

class SensorBase(BaseModel):
    name: str
    location: str

class SensorCreate(SensorBase):
    pass

class SensorUpdate(SensorBase):
    pass

class SensorResponse(SensorBase):
    id: int
    user_id: int

    class Config:
        orm_mode = True

class SensorWithTokenResponse(BaseModel):
    id: UUID
    name: str
    location: str | None
    device_token: str

    class Config:
        from_attributes = True
