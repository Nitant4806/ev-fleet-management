from app.database import SessionLocal

from app.models.vehicle import Vehicle
from app.models.trip import Trip

from app.core.enums import (
    VehicleStatus,
    TripStatus,
)

from datetime import timedelta
from app.services.simulation_clock import (
    get_simulated_time,
)

db = SessionLocal()

vehicles = db.query(Vehicle).filter(Vehicle.id.in_([117, 118, 119, 120])).all()

socs = [5, 8, 12, 15]
departures = [30, 45, 60, 90]

for i, vehicle in enumerate(vehicles):

    vehicle.current_soc = socs[i]
    vehicle.status = VehicleStatus.AVAILABLE

    trip = (
        db.query(Trip)
        .filter(
            Trip.vehicle_id == vehicle.id,
            Trip.status == TripStatus.PENDING,
        )
        .first()
    )

    if trip:

        trip.scheduled_start_at = get_simulated_time() + timedelta(
            minutes=departures[i]
        )

db.commit()

print("Demo scenario seeded.")
