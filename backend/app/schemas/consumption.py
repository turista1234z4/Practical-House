from pydantic import BaseModel
from datetime import datetime
from uuid import UUID

class ConsumptionResponse(BaseModel):
    sensor_id: UUID
    total_kwh: float
    avg_power_w: float | None = None
    start_period: datetime
    end_period: datetime

    class Config:
        from_attributes = True
