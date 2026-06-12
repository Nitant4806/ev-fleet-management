from datetime import datetime, timedelta

from app.models.vehicle import Vehicle
from app.models.trip import Trip

from app.services.risk_monitor_service import (
    evaluate_vehicle_risk,
)

vehicle = Vehicle(
    id=1,
    current_soc=40,
    battery_capacity=40,
    efficiency_kwh_per_km=0.2,
)

trip = Trip(
    id=1,
    distance_km=50,
    scheduled_start_at=datetime.utcnow() + timedelta(hours=2),
)

result = evaluate_vehicle_risk(
    vehicle=vehicle,
    trip=trip,
    drain_rate_per_hour=4,
)

print(result)
