from app.models.vehicle import Vehicle
from app.models.trip import Trip

from app.core.enums import (
    VehicleStatus,
    TripStatus,
)

from app.services.simulation_clock import (
    get_simulated_time,
)


def process_pending_trips(db):

    now = get_simulated_time()

    trips = db.query(Trip).filter(Trip.status == TripStatus.PENDING).all()

    for trip in trips:

        if trip.scheduled_start_at and trip.scheduled_start_at <= now:

            vehicle = db.query(Vehicle).filter(Vehicle.id == trip.vehicle_id).first()

            if vehicle.status != VehicleStatus.AVAILABLE:
                continue

            trip.status = TripStatus.IN_PROGRESS

            trip.started_at = now

            vehicle.status = VehicleStatus.ON_TRIP

    db.commit()
