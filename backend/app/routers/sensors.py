from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.sensors import Sensor
from app.schemas.sensor import SensorCreate, SensorUpdate, SensorResponse
from app.core.auth_utils import get_current_user
import secrets
from uuid import UUID


router = APIRouter(prefix="/sensors", tags=["Sensors"])
device_token = secrets.token_hex(16)

# CRIANDO SENSOR

@router.post("/", response_model=SensorResponse)
def create_sensor(data: SensorCreate, 
                  db: Session = Depends(get_db), 
                  user=Depends(get_current_user)):

    sensor = Sensor(
    name=data.name,
    location=data.location,
    user_id=user.id,
    device_token=device_token
)

    db.add(sensor)
    db.commit()
    db.refresh(sensor)

    return sensor



# LISTANDO SENSORES DAQUELE USUARIO

@router.get("/", response_model=list[SensorResponse])
def list_sensors(db: Session = Depends(get_db), 
                 user=Depends(get_current_user)):

    sensors = db.query(Sensor).filter(Sensor.user_id == user.id).all()
    return sensors



# DANDO GET NUM UNICO SENSOR

@router.get("/{sensor_id}", response_model=SensorResponse)
def get_sensor(sensor_id: int, 
               db: Session = Depends(get_db), 
               user=Depends(get_current_user)):

    sensor = db.query(Sensor).filter(
        Sensor.id == sensor_id,
        Sensor.user_id == user.id
    ).first()

    if not sensor:
        raise HTTPException(404, "Sensor não encontrado")

    return sensor


# DANDO UPDATE NO SENSOR

@router.put("/{sensor_id}", response_model=SensorResponse)
def update_sensor(sensor_id: int, data: SensorUpdate,
                  db: Session = Depends(get_db),
                  user=Depends(get_current_user)):

    sensor = db.query(Sensor).filter(
        Sensor.id == sensor_id,
        Sensor.user_id == user.id
    ).first()

    if not sensor:
        raise HTTPException(404, "Sensor não encontrado")

    sensor.name = data.name
    sensor.location = data.location

    db.commit()
    db.refresh(sensor)
    return sensor

# DELETANDO SENSOR

@router.delete("/{sensor_id}")
def delete_sensor(sensor_id: int, 
                  db: Session = Depends(get_db),
                  user=Depends(get_current_user)):

    sensor = db.query(Sensor).filter(
        Sensor.id == sensor_id,
        Sensor.user_id == user.id
    ).first()

    if not sensor:
        raise HTTPException(404, "Sensor não encontrado")

    db.delete(sensor)
    db.commit()
    return {"message": "Sensor excluído com sucesso"}


@router.post("/{sensor_id}/renew-token")
def renew_device_token(sensor_id: UUID,
                       db: Session = Depends(get_db),
                       user=Depends(get_current_user)):
    
    sensor = db.query(Sensor).filter(
        Sensor.id == sensor_id,
        Sensor.user_id == user.id
    ).first()

    if not sensor:
        raise HTTPException(404, "Sensor não encontrado")

    sensor.device_token = uuid.uuid4().hex

    db.commit()
    db.refresh(sensor)

    return {"device_token": sensor.device_token}