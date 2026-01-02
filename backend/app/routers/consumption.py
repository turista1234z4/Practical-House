from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime, timedelta
from app.core.database import get_db
from app.models.sensor_reading import SensorReading
from app.schemas.consumption import ConsumptionResponse
from uuid import UUID
from fastapi import HTTPException, Depends
from app.core.auth_utils import get_current_user
from app.models.sensors import Sensor

router = APIRouter(prefix="/consumption", tags=["Consumption"])


@router.get("/", response_model=list[ConsumptionResponse])
def get_consumption(
    sensor_id: str | None = None,
    hours: int = Query(default=24, ge=1, le=720),
    db: Session = Depends(get_db)
):
    end_time = datetime.utcnow()
    start_time = end_time - timedelta(hours=hours)

    query = (
        db.query(
            SensorReading.sensor_id.label("sensor_id"),
            func.sum(SensorReading.energy_kwh).label("total_kwh"),
            func.avg(SensorReading.power_w).label("avg_power_w"),
        )
        .filter(SensorReading.timestamp >= start_time)
        .filter(SensorReading.timestamp <= end_time)
    )

    if sensor_id:
        query = query.filter(SensorReading.sensor_id == sensor_id)

    query = query.group_by(SensorReading.sensor_id)

    results = query.all()

    return [
        ConsumptionResponse(
            sensor_id=row.sensor_id,
            total_kwh=row.total_kwh or 0,
            avg_power_w=row.avg_power_w or 0,
            start_period=start_time,
            end_period=end_time,
        )
        for row in results
    ]


@router.get("/{sensor_id}/dashboard")
def sensor_dashboard(
    sensor_id: UUID,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):

    sensor = db.query(Sensor).filter(
        Sensor.id == sensor_id,
        Sensor.user_id == user.id
    ).first()

    if not sensor:
        raise HTTPException(404, "Sensor não encontrado ou não pertence ao usuário")

    now = datetime.utcnow()
    today = now.date()
    seven_days_ago = now - timedelta(days=7)
    thirty_days_ago = now - timedelta(days=30)

    # 🔹 Últimas 20 leituras
    latest_readings = (
        db.query(SensorReading)
        .filter(SensorReading.sensor_id == sensor_id)
        .order_by(SensorReading.timestamp.desc())
        .limit(20)
        .all()
    )

    # 🔹 Consumo do dia
    daily = (
        db.query(
            func.sum(SensorReading.energy_kwh),
            func.avg(SensorReading.power_w)
        )
        .filter(
            SensorReading.sensor_id == sensor_id,
            func.date(SensorReading.timestamp) == today
        )
        .first()
    )

    # 🔹 Últimos 7 dias
    weekly = (
        db.query(
            func.sum(SensorReading.energy_kwh),
            func.avg(SensorReading.power_w)
        )
        .filter(
            SensorReading.sensor_id == sensor_id,
            SensorReading.timestamp >= seven_days_ago
        )
        .first()
    )

    # 🔹 Últimos 30 dias
    monthly = (
        db.query(
            func.sum(SensorReading.energy_kwh),
            func.avg(SensorReading.power_w)
        )
        .filter(
            SensorReading.sensor_id == sensor_id,
            SensorReading.timestamp >= thirty_days_ago
        )
        .first()
    )

    return {
        "sensor": {
            "id": sensor.id,
            "name": sensor.name,
            "location": sensor.location
        },
        "latest_readings": [
            {
                "timestamp": r.timestamp,
                "power_w": r.power_w,
                "energy_kwh": r.energy_kwh,
                "voltage_v": r.voltage_v,
                "current_a": r.current_a
            }
            for r in latest_readings
        ],
        "summary": {
            "today": {
                "total_energy_kwh": daily[0] or 0,
                "avg_power_w": daily[1] or 0
            },
            "last_7_days": {
                "total_energy_kwh": weekly[0] or 0,
                "avg_power_w": weekly[1] or 0
            },
            "last_30_days": {
                "total_energy_kwh": monthly[0] or 0,
                "avg_power_w": monthly[1] or 0
            }
        }
    }
