from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.sensors import Sensor
from app.models.user import User
from app.core.auth_utils import get_current_user
from pydantic import BaseModel

router = APIRouter(prefix="/sensors", tags=["sensors"])


# -----------------------------
# Pydantic Models
# -----------------------------

class SensorCreate(BaseModel):
    name: str
    location: str | None = None


# -----------------------------
# Rotas
# -----------------------------

@router.get("/")
def list_sensors(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    sensors = db.query(Sensor).filter(Sensor.user_id == current_user.id).all()
    return sensors


@router.post("/")
def create_sensor(
    data: SensorCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    new_sensor = Sensor(
        name=data.name,
        location=data.location,
        user_id=current_user.id
    )

    db.add(new_sensor)
    db.commit()
    db.refresh(new_sensor)

    return new_sensor


@router.delete("/{sensor_id}")
def delete_sensor(
    sensor_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    sensor = db.query(Sensor).filter(
        Sensor.id == sensor_id,
        Sensor.user_id == current_user.id
    ).first()

    if not sensor:
        raise HTTPException(status_code=404, detail="Sensor não encontrado")

    db.delete(sensor)
    db.commit()
    return {"message": "Sensor removido com sucesso"}
