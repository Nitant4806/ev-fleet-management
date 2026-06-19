import app.models

from app.database import SessionLocal

from app.models.vehicle import Vehicle
from app.models.trip import Trip
from app.models.charging_station import ChargingStation

from app.core.enums import (
    VehicleStatus,
    TripStatus,
)

from app.services.simulation_clock import (
    reset_simulation_time,
)

db = SessionLocal()

# Force mapper initialization
_ = ChargingStation

vehicles = db.query(Vehicle).all()

for vehicle in vehicles:

    vehicle.status = VehicleStatus.AVAILABLE

    vehicle.charging_station_id = None

    vehicle.target_soc = None

db.commit()

trips = db.query(Trip).all()

for trip in trips:

    trip.status = TripStatus.PENDING

    trip.started_at = None

    trip.completed_at = None

db.commit()

reset_simulation_time()

print("Simulation world reset")
