# test_state_machine.py

from app.core.enums import VehicleStatus

from app.services.simulator_service import (
    dispatch_vehicle,
    start_trip,
    complete_trip,
)

status = VehicleStatus.AVAILABLE

print(status)

status = dispatch_vehicle(status)
print(status)

status = start_trip(status)
print(status)

status = complete_trip(status)
print(status)
