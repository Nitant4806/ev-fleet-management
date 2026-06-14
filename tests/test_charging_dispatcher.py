from app.database import SessionLocal

from app.models.vehicle import Vehicle
from app.models.charging_station import ChargingStation

from app.core.enums import (
    VehicleStatus,
)

from app.services.charging_dispatcher import (
    assign_vehicle_to_station,
)

db = SessionLocal()

vehicle = db.query(Vehicle).filter(Vehicle.status == VehicleStatus.AVAILABLE).first()

station = db.query(ChargingStation).first()

print("Before")
print("Vehicle Status:", vehicle.status)
print("Station:", station.name)
print(
    "Available Chargers:",
    station.available_chargers,
)

success = assign_vehicle_to_station(
    db=db,
    vehicle=vehicle,
    station=station,
)

db.refresh(vehicle)
db.refresh(station)

print()
print("Assignment Success:", success)

print()
print("After")
print("Vehicle Status:", vehicle.status)

print(
    "Charging Station ID:",
    vehicle.charging_station_id,
)

print(
    "Charging Station Name:",
    vehicle.charging_station.name,
)

print(
    "Available Chargers:",
    station.available_chargers,
)
