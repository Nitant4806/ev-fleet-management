from app.database import SessionLocal
from app.models.vehicle import Vehicle
from datetime import timedelta
from app.models.vehicle import Vehicle
from app.models.trip import Trip

from app.services.risk_monitor_service import (
    evaluate_vehicle_risk,
)

db = SessionLocal()

trips = db.query(Trip).filter(Trip.status == "pending").limit(10).all()

for trip in trips:

    vehicle = db.query(Vehicle).filter(Vehicle.id == trip.vehicle_id).first()

    risk = evaluate_vehicle_risk(
        vehicle=vehicle,
        trip=trip,
        drain_rate_per_hour=4,
    )

    print()

    print("Vehicle:", vehicle.id)
    print("Trip:", trip.id)
    print("SOC:", vehicle.current_soc)
    print("Required:", risk["required_soc"])
    print("Projected:", risk["projected_soc"])
    print("Deficit:", risk["deficit"])
    print("Risk:", risk["risk_score"])
