from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db

from app.services.simulation_runner import (
    process_fleet_risks,
)

from app.services.fleet_priority_service import (
    build_priority_queue,
)
from app.models.vehicle import Vehicle

from app.core.enums import (
    VehicleStatus,
)

router = APIRouter(
    prefix="/fleet",
    tags=["Fleet"],
)


@router.get("/priorities")
def get_priorities(
    db: Session = Depends(get_db),
):

    recommendations = process_fleet_risks(db)

    queue = build_priority_queue(recommendations)

    return queue


@router.get("/charging")
def charging_vehicles(
    db: Session = Depends(get_db),
):

    vehicles = db.query(Vehicle).filter(Vehicle.status == VehicleStatus.CHARGING).all()

    return [
        {
            "vehicle_id": v.id,
            "soc": v.current_soc,
            "station_id": (v.charging_station_id),
        }
        for v in vehicles
    ]
