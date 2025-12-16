from fastapi import Header, HTTPException, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.sensor import Sensor

def get_current_sensor(
    x_device_token: str = Header(...),
    db: Session = Depends(get_db)
):
    sensor = db.query(Sensor).filter(
        Sensor.device_token == x_device_token
    ).first()

    if not sensor:
        raise HTTPException(
            status_code=401,
            detail="Invalid device token"
        )

    return sensor
