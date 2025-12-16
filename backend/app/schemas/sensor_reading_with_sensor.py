from pydantic import BaseModel
from uuid import UUID
from datetime import datetime


class SensorInfo(BaseModel):
    id: UUID
    name: str
    location: str | None

    class Config:
        from_attributes = True


class SensorReadingWithSensorResponse(BaseModel):
    id: UUID
    energy_kwh: float
    current_a: float
    voltage_v: float
    power_w: float
    created_at: datetime
    sensor: SensorInfo

    class Config:
        from_attributes = True
