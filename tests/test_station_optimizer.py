from app.models.vehicle import Vehicle
from app.models.charging_station import ChargingStation

from app.services.station_service import (
    find_best_station,
)

vehicle = Vehicle(
    battery_capacity=40,
    location_name="Gift City",
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

result = find_best_station(
    vehicle=vehicle,
    stations=stations,
    soc_needed=20,
)

print(result)
