from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db

from app.models.charging_station import (
    ChargingStation,
)

router = APIRouter(
    prefix="/stations",
    tags=["Stations"],
)


@router.get("/status")
def station_status(
    db: Session = Depends(get_db),
):

    stations = db.query(ChargingStation).all()

    return [
        {
            "id": station.id,
            "name": station.name,
            "available_chargers": station.available_chargers,
            "total_chargers": station.total_chargers,
            "queue_time": station.avg_queue_minutes,
        }
        for station in stations
    ]
