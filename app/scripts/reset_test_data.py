from app.database import SessionLocal

from app.models.vehicle import Vehicle
from app.models.vehicle import Vehicle
from app.models.charging_station import ChargingStation
from app.core.enums import (
    VehicleStatus,
)

db = SessionLocal()

vehicles = db.query(Vehicle).all()

for vehicle in vehicles:

    vehicle.status = VehicleStatus.AVAILABLE

    vehicle.charging_station_id = None

    vehicle.target_soc = None

db.commit()

print("Reset complete")
