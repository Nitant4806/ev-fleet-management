from app.models.vehicle import Vehicle
from app.models.charging_station import ChargingStation

from app.core.enums import (
    VehicleStatus,
)

CHARGING_RATE_PER_CYCLE = 10


def start_charging_session(
    vehicle: Vehicle,
    station: ChargingStation,
):

    if vehicle.status == VehicleStatus.CHARGING:
        return

    vehicle.status = VehicleStatus.CHARGING


def process_charging_sessions(db):

    vehicles = db.query(Vehicle).filter(Vehicle.status == VehicleStatus.CHARGING).all()

    for vehicle in vehicles:

        vehicle.current_soc += CHARGING_RATE_PER_CYCLE

        vehicle.current_soc = min(
            100,
            round(
                vehicle.current_soc,
                2,
            ),
        )

        if vehicle.current_soc >= 80:

            station = vehicle.charging_station

            if station:

                station.available_chargers += 1

            vehicle.charging_station_id = None

            vehicle.status = VehicleStatus.AVAILABLE

            
           
    db.commit()
