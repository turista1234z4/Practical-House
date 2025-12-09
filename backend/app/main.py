from fastapi import FastAPI
from app.core.database import Base, engine
from app.routers.auth import router as auth_router
from app.routers.sensors import router as sensors_router
from app.models import User, Sensor, SensorReading
from app.routers.sensor_reading import router as sensor_readings_router





app = FastAPI()

app.include_router(auth_router)
app.include_router(sensors_router)
app.include_router(sensor_readings_router)

@app.on_event("startup")
async def startup_event():
    Base.metadata.create_all(bind=engine)


@app.get("/")
def root():
    return {"message": "backend is running"}

