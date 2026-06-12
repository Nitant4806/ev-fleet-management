from app.models.vehicle import Vehicle
from app.models.trip import Trip

from app.core.enums import (
    VehicleStatus,
)

from app.services.simulator_service import (
    simulate_trip,
)

vehicle = Vehicle(
    current_soc=75,
    battery_capacity=40,
    efficiency_kwh_per_km=0.2,
    location_name="Gift City",
    status=VehicleStatus.AVAILABLE,
)

trip = Trip(
    distance_km=20,
    destination="DAIICT",
)

simulate_trip(
    vehicle,
    trip,
)

print(vehicle.current_soc)
print(vehicle.location_name)
print(vehicle.status)
