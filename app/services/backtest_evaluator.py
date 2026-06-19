from app.models.trip import Trip
from app.models.vehicle import Vehicle
from app.models.charging_station import ChargingStation

from app.core.enums import (
    TripStatus,
    VehicleStatus,
)


def count_completed_trips(db):

    return db.query(Trip).filter(Trip.status == TripStatus.COMPLETED).count()


def count_charging_vehicles(db):

    return db.query(Vehicle).filter(Vehicle.status == VehicleStatus.CHARGING).count()


def calculate_average_station_queue(
    db,
):

    stations = db.query(ChargingStation).all()

    if not stations:
        return 0

    total = sum(station.avg_queue_minutes for station in stations)

    return round(
        total / len(stations),
        2,
    )


def calculate_utilization(
    db,
):

    stations = db.query(ChargingStation).all()

    total_chargers = 0

    occupied_chargers = 0

    for station in stations:

        total_chargers += station.total_chargers

        occupied_chargers += station.total_chargers - station.available_chargers

    if total_chargers == 0:
        return 0

    return round(
        (occupied_chargers / total_chargers) * 100,
        2,
    )


def count_missed_trips(db):

    return db.query(Trip).filter(Trip.status == TripStatus.PENDING).count()
