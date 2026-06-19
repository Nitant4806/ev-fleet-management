from app.database import SessionLocal

from app.models.vehicle import Vehicle
from app.models.charging_station import ChargingStation

from app.core.enums import (
    VehicleStatus,
)

from app.services.queue_service import (
    calculate_station_queue_time,
)

db = SessionLocal()

station = db.query(ChargingStation).first()

if station is None:
    print("No station found")
    exit()

vehicles = db.query(Vehicle).limit(3).all()

if len(vehicles) < 3:
    print("Need at least 3 vehicles")
    exit()

vehicle_a = vehicles[0]
vehicle_b = vehicles[1]
vehicle_c = vehicles[2]

vehicle_a.status = VehicleStatus.CHARGING
vehicle_a.charging_station_id = station.id
vehicle_a.current_soc = 30
vehicle_a.target_soc = 40

vehicle_b.status = VehicleStatus.CHARGING
vehicle_b.charging_station_id = station.id
vehicle_b.current_soc = 20
vehicle_b.target_soc = 70

vehicle_c.status = VehicleStatus.CHARGING
vehicle_c.charging_station_id = station.id
vehicle_c.current_soc = 60
vehicle_c.target_soc = 80

station.available_chargers = station.total_chargers - 3

db.commit()

print("===== CHARGING VEHICLES =====")
print()

print(f"Vehicle {vehicle_a.id}")
print(f"Current: {vehicle_a.current_soc}")
print(f"Target: {vehicle_a.target_soc}")
print(f"Remaining: " f"{vehicle_a.target_soc - vehicle_a.current_soc}")
print()

print(f"Vehicle {vehicle_b.id}")
print(f"Current: {vehicle_b.current_soc}")
print(f"Target: {vehicle_b.target_soc}")
print(f"Remaining: " f"{vehicle_b.target_soc - vehicle_b.current_soc}")
print()

print(f"Vehicle {vehicle_c.id}")
print(f"Current: {vehicle_c.current_soc}")
print(f"Target: {vehicle_c.target_soc}")
print(f"Remaining: " f"{vehicle_c.target_soc - vehicle_c.current_soc}")
print()

queue_time = calculate_station_queue_time(
    db,
    station,
)

print("===== RESULT =====")
print(
    "Station:",
    station.name,
)
print(
    "Dynamic Queue Time:",
    queue_time,
    "minutes",
)
