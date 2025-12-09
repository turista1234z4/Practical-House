from pydantic import BaseModel
from uuid import UUID
from datetime import datetime

class SensorReadingBase(BaseModel):
    energy_kwh: float | None = None
    current_a: float | None = None
    voltage_v: float | None = None
    power_w: float | None = None


class SensorReadingCreate(SensorReadingBase):
    pass


class SensorReadingResponse(SensorReadingBase):
    id: UUID
    sensor_id: UUID
    timestamp: datetime

    class Config:
        from_attributes = True
