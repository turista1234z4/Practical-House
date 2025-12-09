from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from uuid import UUID
from datetime import datetime, date, timedelta
from sqlalchemy import func

from app.core.database import get_db
from app.core.auth_utils import get_current_user
from app.models.sensor_reading import SensorReading
from app.models.sensors import Sensor
from app.schemas.sensor_reading import SensorReadingCreate, SensorReadingResponse

router = APIRouter(prefix="/sensor-readings", tags=["Sensor Readings"])


# -----------------------------------------
# Criar leitura
# -----------------------------------------

@router.post("/{sensor_id}", response_model=SensorReadingResponse)
def create_reading(sensor_id: UUID,
                   data: SensorReadingCreate,
                   db: Session = Depends(get_db),
                   user=Depends(get_current_user)):

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


# -----------------------------------------
# Listar leituras
# -----------------------------------------

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


# -----------------------------------------
# Estatísticas por hora (dia específico)
# -----------------------------------------

@router.get("/{sensor_id}/by-hour")
def hourly_stats(sensor_id: UUID,
                 date_filter: date,
                 db: Session = Depends(get_db),
                 user=Depends(get_current_user)):

    sensor = db.query(Sensor).filter(
        Sensor.id == sensor_id,
        Sensor.user_id == user.id
    ).first()

    if not sensor:
        raise HTTPException(404, "Sensor não encontrado ou não pertence ao usuário")

    results = (
        db.query(
            func.extract("hour", SensorReading.timestamp).label("hour"),
            func.avg(SensorReading.power_w).label("avg_power"),
            func.sum(SensorReading.energy_kwh).label("total_energy")
        )
        .filter(
            SensorReading.sensor_id == sensor_id,
            func.date(SensorReading.timestamp) == date_filter
        )
        .group_by(func.extract("hour", SensorReading.timestamp))
        .order_by("hour")
        .all()
    )

    return [
        {
            "hour": int(r.hour),
            "average_power_w": r.avg_power,
            "total_energy_kwh": r.total_energy
        }
        for r in results
    ]


# -----------------------------------------
# Estatísticas diárias (todos os dias)
# -----------------------------------------

@router.get("/{sensor_id}/daily")
def daily_stats(sensor_id: UUID,
                db: Session = Depends(get_db),
                user=Depends(get_current_user)):

    sensor = db.query(Sensor).filter(
        Sensor.id == sensor_id,
        Sensor.user_id == user.id
    ).first()

    if not sensor:
        raise HTTPException(404, "Sensor não encontrado ou não pertence ao usuário")

    results = (
        db.query(
            func.date(SensorReading.timestamp).label("day"),
            func.avg(SensorReading.power_w).label("avg_power"),
            func.sum(SensorReading.energy_kwh).label("total_energy")
        )
        .filter(SensorReading.sensor_id == sensor_id)
        .group_by(func.date(SensorReading.timestamp))
        .order_by(func.date(SensorReading.timestamp))
        .all()
    )

    return [
        {
            "date": str(r.day),
            "average_power_w": r.avg_power,
            "total_energy_kwh": r.total_energy
        }
        for r in results
    ]


# -----------------------------------------
# Estatísticas semanais (últimos 7 dias)
# -----------------------------------------

@router.get("/{sensor_id}/weekly")
def weekly_chart(sensor_id: UUID,
                 db: Session = Depends(get_db),
                 user=Depends(get_current_user)):

    sensor = db.query(Sensor).filter(
        Sensor.id == sensor_id,
        Sensor.user_id == user.id
    ).first()

    if not sensor:
        raise HTTPException(404, "Sensor não encontrado ou não pertence ao usuário")

    seven_days_ago = datetime.utcnow() - timedelta(days=7)

    readings = (
        db.query(
            func.date(SensorReading.timestamp).label("day"),
            func.avg(SensorReading.energy_kwh).label("energy_kwh"),
            func.avg(SensorReading.power_w).label("power_w")
        )
        .filter(
            SensorReading.sensor_id == sensor_id,
            SensorReading.timestamp >= seven_days_ago
        )
        .group_by(func.date(SensorReading.timestamp))
        .order_by(func.date(SensorReading.timestamp))
        .all()
    )

    return [
        {
            "day": r.day,
            "energy_kwh": r.energy_kwh,
            "power_w": r.power_w
        }
        for r in readings
    ]


# -----------------------------------------
# Estatísticas mensais (últimos 30 dias)
# -----------------------------------------

@router.get("/{sensor_id}/monthly")
def monthly_chart(sensor_id: UUID,
                  db: Session = Depends(get_db),
                  user=Depends(get_current_user)):

    sensor = db.query(Sensor).filter(
        Sensor.id == sensor_id,
        Sensor.user_id == user.id
    ).first()

    if not sensor:
        raise HTTPException(404, "Sensor não encontrado ou não pertence ao usuário")

    thirty_days_ago = datetime.utcnow() - timedelta(days=30)

    readings = (
        db.query(
            func.date(SensorReading.timestamp).label("day"),
            func.avg(SensorReading.energy_kwh).label("energy_kwh"),
            func.avg(SensorReading.power_w).label("power_w")
        )
        .filter(
            SensorReading.sensor_id == sensor_id,
            SensorReading.timestamp >= thirty_days_ago
        )
        .group_by(func.date(SensorReading.timestamp))
        .order_by(func.date(SensorReading.timestamp))
        .all()
    )

    return [
        {
            "day": r.day,
            "energy_kwh": r.energy_kwh,
            "power_w": r.power_w
        }
        for r in readings
    ]
