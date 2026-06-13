from app.database import SessionLocal

from app.models.vehicle import Vehicle
from app.models.trip import Trip

from app.services.risk_monitor_service import (
    evaluate_vehicle_risk,
)

from app.services.simulation_clock import (
    get_simulated_time,
)

db = SessionLocal()

vehicle_id = 127

vehicle = db.query(Vehicle).filter(Vehicle.id == vehicle_id).first()

vehicle.current_soc = 15

db.commit()

trip = (
    db.query(Trip)
    .filter(
        Trip.vehicle_id == vehicle.id,
        Trip.status == "pending",
    )
    .order_by(Trip.scheduled_start_at)
    .first()
)

risk = evaluate_vehicle_risk(
    vehicle=vehicle,
    trip=trip,
)

print("Vehicle:", vehicle.id)
print("Current SOC:", vehicle.current_soc)

print()
print("Trip:", trip.id)
print("Distance:", trip.distance_km)
print("Departure:", trip.scheduled_start_at)

print()
print("Required SOC:", risk["required_soc"])
print("Projected SOC:", risk["projected_soc"])
print("Deficit:", risk["deficit"])
print("Risk Score:", risk["risk_score"])

print()
print("Simulation Time:")
print(get_simulated_time())
