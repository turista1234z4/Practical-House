from fastapi import APIRouter, Depends, HTTPException, Header
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.sensors import Sensor
from app.schemas.sensor_reading import SensorReadingCreate, SensorReadingResponse
from app.models.sensor_reading import SensorReading

router = APIRouter(prefix="/device", tags=["Device"])


def get_sensor_by_token(db: Session, token: str):
    sensor = db.query(Sensor).filter(Sensor.device_token == token).first()
    if not sensor:
        raise HTTPException(status_code=401, detail="Token do dispositivo inválido")
    return sensor


@router.post("/send-reading", response_model=SensorReadingResponse)
def device_send_reading(
    data: SensorReadingCreate,
    x_device_token: str = Header(..., alias="X-Device-Token"),
    db: Session = Depends(get_db)
):
    sensor = get_sensor_by_token(db, x_device_token)

    reading = SensorReading(
        sensor_id=sensor.id,
        energy_kwh=data.energy_kwh,
        current_a=data.current_a,
        voltage_v=data.voltage_v,
        power_w=data.power_w
    )

    db.add(reading)
    db.commit()
    db.refresh(reading)

    return reading
