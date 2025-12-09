from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from uuid import UUID

from app.core.database import get_db
from app.core.auth_utils import get_current_user
from app.models.sensor_reading import SensorReading
from app.models.sensors import Sensor
from app.schemas.sensor_reading import SensorReadingCreate, SensorReadingResponse

router = APIRouter(prefix="/sensor-readings", tags=["Sensor Readings"])


# CRIAR LEITURA

@router.post("/{sensor_id}", response_model=SensorReadingResponse)
def create_reading(sensor_id: UUID,
                   data: SensorReadingCreate,
                   db: Session = Depends(get_db),
                   user=Depends(get_current_user)):

    # Só pode criar leitura de sensor do próprio dono
    sensor = db.query(Sensor).filter(
        Sensor.id == sensor_id,
        Sensor.user_id == user.id
    ).first()

    if not sensor:
        raise HTTPException(404, "Sensor não encontrado ou não pertence ao usuário")

    reading = SensorReading(
        sensor_id=sensor_id,
        energy_kwh=data.energy_kwh,
        current_a=data.current_a,
        voltage_v=data.voltage_v,
        power_w=data.power_w,
    )

    db.add(reading)
    db.commit()
    db.refresh(reading)

    return reading


# LISTAR TODAS AS LEITURAS DE UM SENSOR

@router.get("/{sensor_id}", response_model=list[SensorReadingResponse])
def list_readings(sensor_id: UUID,
                  db: Session = Depends(get_db),
                  user=Depends(get_current_user)):

    sensor = db.query(Sensor).filter(
        Sensor.id == sensor_id,
        Sensor.user_id == user.id
    ).first()

    if not sensor:
        raise HTTPException(404, "Sensor não encontrado ou não pertence ao usuário")

    readings = db.query(SensorReading).filter(
        SensorReading.sensor_id == sensor_id
    ).order_by(SensorReading.timestamp.desc()).all()

    return readings
