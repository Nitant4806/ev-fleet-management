from app.models.vehicle import Vehicle
from app.models.charging_station import ChargingStation

from app.core.enums import (
    VehicleStatus,
)


def assign_vehicle_to_station(
    db,
    vehicle: Vehicle,
    station: ChargingStation,
) -> bool:

    if station.available_chargers <= 0:
        return False

    station.available_chargers -= 1

    vehicle.status = VehicleStatus.CHARGING

    vehicle.charging_station_id = station.id

    db.commit()

    return True
