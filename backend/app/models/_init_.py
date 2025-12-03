from app.core.database import Base

# importe todos os modelos aqui
from app.models.user import User  # adicione conforme criar modelos
from .user import User
from .sensors import Sensor
from .sensor_reading import SensorReading
