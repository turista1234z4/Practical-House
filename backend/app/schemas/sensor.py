from pydantic import BaseModel

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
