from app.services.event_service import (
    publish_event,
)

from app.models.vehicle import Vehicle
from app.models.charging_station import ChargingStation

from app.core.enums import (
    VehicleStatus,
)

CHARGING_RATE_PER_CYCLE = 10


def start_charging_session(
    vehicle: Vehicle,
    station: ChargingStation,
    target_soc: float,
):

    if vehicle.status == VehicleStatus.CHARGING:
        return

    vehicle.status = VehicleStatus.CHARGING

    vehicle.target_soc = target_soc

    publish_event(
        {
            "event": "charging_started",
            "vehicle_id": vehicle.id,
            "vehicle_number": vehicle.vehicle_number,
            "station": station.name,
            "target_soc": target_soc,
        }
    )
    publish_event(
        {
            "event": "station_utilization_updated",
            "station": station.name,
            "available_chargers": station.available_chargers,
            "total_chargers": station.total_chargers,
        }
    )


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

        if vehicle.target_soc and vehicle.current_soc >= vehicle.target_soc:

            station = vehicle.charging_station

            if station:

                station.available_chargers = min(
                    station.total_chargers,
                    station.available_chargers + 1,
                )

                publish_event(
                    {
                        "event": "station_utilization_updated",
                        "station": station.name,
                        "available_chargers": station.available_chargers,
                        "total_chargers": station.total_chargers,
                    }
                )

            vehicle.charging_station_id = None

            vehicle.target_soc = None

            vehicle.status = VehicleStatus.AVAILABLE

            publish_event(
                {
                    "event": "charging_completed",
                    "vehicle_id": vehicle.id,
                    "vehicle_number": vehicle.vehicle_number,
                    "soc": vehicle.current_soc,
                }
            )

            publish_event(
                {
                    "event": "vehicle_available",
                    "vehicle_id": vehicle.id,
                    "vehicle_number": vehicle.vehicle_number,
                }
            )

    db.commit()
