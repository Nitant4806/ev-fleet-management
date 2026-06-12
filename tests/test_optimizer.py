from datetime import datetime, timedelta

from app.models.vehicle import Vehicle
from app.models.trip import Trip
from app.models.charging_station import ChargingStation

from app.services.charging_optimizer_service import (
    generate_charging_recommendation,
)

vehicle = Vehicle(
    id=1,
    battery_capacity=40,
    current_soc=30,
    efficiency_kwh_per_km=0.2,
    location_name="Gift City",
)

trip = Trip(
    id=1,
    distance_km=50,
    scheduled_start_at=datetime.utcnow() + timedelta(minutes=60),
)

stations = [
    ChargingStation(
        name="Gift City Supercharger",
        location_name="Gift City",
        max_power_kw=120,
        avg_queue_minutes=5,
    ),
    ChargingStation(
        name="DAIICT Charging Point",
        location_name="DAIICT",
        max_power_kw=30,
        avg_queue_minutes=20,
    ),
]

result = generate_charging_recommendation(
    vehicle=vehicle,
    trip=trip,
    stations=stations,
)

print(result)
