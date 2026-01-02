from fastapi import FastAPI
from app.routers.auth import router as auth_router
from app.routers.sensors import router as sensors_router
from app.routers.sensor_reading import router as sensor_readings_router
from app.routers import device
from app.routers import consumption
from app.routers.consumption import router as consumption_router

app = FastAPI()

app.include_router(auth_router)
app.include_router(sensors_router)
app.include_router(sensor_readings_router)
app.include_router(device.router)
app.include_router(consumption.router)
app.include_router(consumption_router)

@app.get("/")
def root():
    return {"message": "backend is running"}
