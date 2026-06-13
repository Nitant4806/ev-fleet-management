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
    process_pending_trips,
)

db = SessionLocal()

trip = db.query(Trip).filter(Trip.status == TripStatus.PENDING).first()

if trip is None:
    print("No pending trip found")
    exit()

trip.scheduled_start_at = get_simulated_time() - timedelta(minutes=1)

db.commit()

vehicle = db.query(Vehicle).filter(Vehicle.id == trip.vehicle_id).first()

print("Before:")
print("Trip:", trip.status)
print("Vehicle:", vehicle.status)

vehicle.status = VehicleStatus.AVAILABLE
db.commit()

process_pending_trips(db)

db.refresh(trip)
db.refresh(vehicle)

print("\nAfter:")
print("Trip:", trip.status)
print("Vehicle:", vehicle.status)
