from datetime import timedelta

from app.database import SessionLocal

from app.models.trip import Trip
from app.models.vehicle import Vehicle

from app.core.enums import (
    TripStatus,
    VehicleStatus,
)

from app.services.simulation_clock import (
    get_simulated_time,
)

from app.services.simulation_runner import (
    run_simulation_cycle,
)

db = SessionLocal()

trip = db.query(Trip).filter(Trip.status == TripStatus.PENDING).first()

if trip is None:
    print("No pending trip found")
    exit()

vehicle = db.query(Vehicle).filter(Vehicle.id == trip.vehicle_id).first()

vehicle.status = VehicleStatus.AVAILABLE

trip.scheduled_start_at = get_simulated_time() - timedelta(minutes=1)

db.commit()

print("\n===== START TEST =====")

print("Before Start")
print("Trip:", trip.status)
print("Vehicle:", vehicle.status)

run_simulation_cycle(db)

db.refresh(trip)
db.refresh(vehicle)

print("\nAfter Dispatch")
print("Trip:", trip.status)
print("Vehicle:", vehicle.status)
print("Expected End:", trip.expected_end_at)

trip.expected_end_at = get_simulated_time() - timedelta(minutes=1)

db.commit()

run_simulation_cycle(db)

db.refresh(trip)
db.refresh(vehicle)

print("\nAfter Completion")
print("Trip:", trip.status)
print("Vehicle:", vehicle.status)
print("Location:", vehicle.location_name)
print("SOC:", vehicle.current_soc)

print("\n===== END TEST =====")
