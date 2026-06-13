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
    process_completed_trips,
)

db = SessionLocal()

trip = db.query(Trip).filter(Trip.status == TripStatus.IN_PROGRESS).first()

if trip is None:
    print("No in-progress trip found")
    exit()

trip.expected_end_at = get_simulated_time() - timedelta(minutes=1)

db.commit()

vehicle = db.query(Vehicle).filter(Vehicle.id == trip.vehicle_id).first()

print("Before:")
print("Trip:", trip.status)
print("Vehicle:", vehicle.status)
print("Location:", vehicle.location_name)
print("SOC:", vehicle.current_soc)
print("Status:", vehicle.status)

process_completed_trips(db)

db.refresh(trip)
db.refresh(vehicle)

print("\nAfter:")
print("Trip:", trip.status)
print("Vehicle:", vehicle.status)
print("Location:", vehicle.location_name)
print("SOC:", vehicle.current_soc)
print("Status:", vehicle.status)
