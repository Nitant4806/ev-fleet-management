from app.database import SessionLocal

from app.models.vehicle import Vehicle
from app.models.charging_station import ChargingStation

from app.core.enums import (
    VehicleStatus,
)

from app.services.charging_dispatcher import (
    assign_vehicle_to_station,
)

from app.services.charging_session_runner import (
    process_charging_sessions,
)
from app.services.charging_target_service import (
    calculate_target_soc,
)

db = SessionLocal()

vehicle = db.query(Vehicle).filter(Vehicle.status == VehicleStatus.AVAILABLE).first()

station = db.query(ChargingStation).first()

if vehicle is None:
    print("No available vehicle found")
    exit()

if station is None:
    print("No charging station found")
    exit()

vehicle.current_soc = 15

vehicle.target_soc = None

vehicle.status = VehicleStatus.AVAILABLE

vehicle.charging_station_id = None

db.commit()

target_soc = 39

print("===== BEFORE CHARGING =====")
print("Vehicle:", vehicle.id)
print("Current SOC:", vehicle.current_soc)
print("Target SOC:", target_soc)
print("Status:", vehicle.status)
print()

assign_vehicle_to_station(
    db=db,
    vehicle=vehicle,
    station=station,
    target_soc=target_soc,
)

cycle = 1

while True:

    db.refresh(vehicle)

    print(f"===== CYCLE {cycle} =====")

    process_charging_sessions(db)

    db.refresh(vehicle)

    print("SOC:", vehicle.current_soc)
    print("Status:", vehicle.status)
    print("Target SOC:", vehicle.target_soc)

    print()

    if vehicle.status == VehicleStatus.AVAILABLE:
        break

    cycle += 1

print("===== FINAL STATE =====")
print("SOC:", vehicle.current_soc)
print("Status:", vehicle.status)
print("Target SOC:", vehicle.target_soc)
print("Charging Station:", vehicle.charging_station_id)
