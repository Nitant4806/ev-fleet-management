from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.database import get_db

from app.models.vehicle import Vehicle
from app.models.charging_station import ChargingStation

from app.core.enums import (
    VehicleStatus,
)
from app.services.cache_service import (
    get_cache,
    set_cache,
)

router = APIRouter(
    prefix="/analytics",
    tags=["Analytics"],
)


@router.get("/fleet")
def fleet_analytics(
    db: Session = Depends(get_db),
):

    CACHE_KEY = "fleet:analytics"

    cached = get_cache(CACHE_KEY)

    if cached:
        return cached

    total_vehicles = db.query(Vehicle).count()

    available = (
        db.query(Vehicle).filter(Vehicle.status == VehicleStatus.AVAILABLE).count()
    )

    charging = (
        db.query(Vehicle).filter(Vehicle.status == VehicleStatus.CHARGING).count()
    )

    on_trip = db.query(Vehicle).filter(Vehicle.status == VehicleStatus.ON_TRIP).count()

    returned = (
        db.query(Vehicle).filter(Vehicle.status == VehicleStatus.RETURNED).count()
    )

    avg_soc = db.query(func.avg(Vehicle.current_soc)).scalar()

    result = {
        "total_vehicles": total_vehicles,
        "available": available,
        "charging": charging,
        "on_trip": on_trip,
        "returned": returned,
        "average_soc": round(
            avg_soc or 0,
            2,
        ),
    }

    set_cache(
        CACHE_KEY,
        result,
        ttl=30,
    )

    return result


@router.get("/stations")
def station_analytics(
    db: Session = Depends(get_db),
):

    CACHE_KEY = "stations:analytics"

    cached = get_cache(CACHE_KEY)

    if cached:
        return cached

    stations = db.query(ChargingStation).all()

    result = []

    for station in stations:

        occupied = station.total_chargers - station.available_chargers

        utilization = round(
            (occupied / station.total_chargers) * 100,
            2,
        )

        result.append(
            {
                "station_id": station.id,
                "station_name": station.name,
                "available_chargers": station.available_chargers,
                "occupied_chargers": occupied,
                "utilization_percent": utilization,
                "queue_time": station.avg_queue_minutes,
            }
        )

    set_cache(
        CACHE_KEY,
        result,
        ttl=30,
    )

    return result
