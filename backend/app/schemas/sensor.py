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
    id: UUID  
    user_id: UUID  

    class Config:
        orm_mode = True

class SensorWithTokenResponse(BaseModel):
    id: UUID
    name: str
    location: str | None
    device_token: str

    class Config:
        from_attributes = True
        
class SensorDeviceTokenResponse(BaseModel):
    device_token: str