from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db

from app.services.simulation_runner import (
    run_simulation_cycle,
)
from app.models.vehicle import Vehicle
from app.models.trip import Trip

from app.core.enums import (
    VehicleStatus,
    TripStatus,
)

router = APIRouter(
    prefix="/simulation",
    tags=["Simulation"],
)


@router.post("/run-cycle")
def run_cycle(
    db: Session = Depends(get_db),
):

    priority_queue = run_simulation_cycle(db)

    return {
        "message": "Simulation cycle completed",
        "priority_count": len(priority_queue),
    }


@router.get("/status")
def simulation_status(
    db: Session = Depends(get_db),
):

    vehicles = db.query(Vehicle).count()

    trips = db.query(Trip).count()

    charging = (
        db.query(Vehicle).filter(Vehicle.status == VehicleStatus.CHARGING).count()
    )

    active_trips = db.query(Trip).filter(Trip.status == TripStatus.IN_PROGRESS).count()

    return {
        "vehicles": vehicles,
        "trips": trips,
        "charging_vehicles": charging,
        "active_trips": active_trips,
    }
