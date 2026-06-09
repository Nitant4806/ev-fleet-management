from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.charging_session import ChargingSession
from app.models.charging_station import ChargingStation
from app.models.vehicle import Vehicle
from app.schemas.charging_session import (
    ChargingSessionCreate,
    ChargingSessionUpdate,
)

router = APIRouter()


@router.post("/charging-sessions")
def create_charging_session(
    session: ChargingSessionCreate,
    db: Session = Depends(get_db),
):
    vehicle = db.query(Vehicle).filter(Vehicle.id == session.vehicle_id).first()

    if vehicle is None:
        raise HTTPException(
            status_code=404,
            detail="Vehicle not found",
        )

    station = (
        db.query(ChargingStation)
        .filter(ChargingStation.id == session.station_id)
        .first()
    )

    if station is None:
        raise HTTPException(
            status_code=404,
            detail="Station not found",
        )

    if session.target_soc <= session.start_soc:
        raise HTTPException(
            status_code=400,
            detail="target_soc must be greater than start_soc",
        )

    new_session = ChargingSession(
        vehicle_id=session.vehicle_id,
        station_id=session.station_id,
        start_soc=session.start_soc,
        target_soc=session.target_soc,
        status=session.status,
    )

    db.add(new_session)
    db.commit()
    db.refresh(new_session)

    return {
        "message": "Charging session created successfully",
        "id": new_session.id,
    }


@router.get("/charging-sessions")
def get_charging_sessions(
    db: Session = Depends(get_db),
):
    return db.query(ChargingSession).all()


@router.get("/charging-sessions/{session_id}")
def get_charging_session(
    session_id: int,
    db: Session = Depends(get_db),
):
    session = db.query(ChargingSession).filter(ChargingSession.id == session_id).first()

    if session is None:
        raise HTTPException(
            status_code=404,
            detail="Charging session not found",
        )

    return session


@router.put("/charging-sessions/{session_id}")
def update_charging_session(
    session_id: int,
    session_data: ChargingSessionUpdate,
    db: Session = Depends(get_db),
):
    session = db.query(ChargingSession).filter(ChargingSession.id == session_id).first()

    if session is None:
        raise HTTPException(
            status_code=404,
            detail="Charging session not found",
        )

    if session_data.target_soc <= session_data.start_soc:
        raise HTTPException(
            status_code=400,
            detail="target_soc must be greater than start_soc",
        )

    for field, value in session_data.model_dump().items():
        setattr(session, field, value)

    db.commit()
    db.refresh(session)

    return {
        "message": "Charging session updated successfully",
        "id": session.id,
    }


@router.delete("/charging-sessions/{session_id}")
def delete_charging_session(
    session_id: int,
    db: Session = Depends(get_db),
):
    session = db.query(ChargingSession).filter(ChargingSession.id == session_id).first()

    if session is None:
        raise HTTPException(
            status_code=404,
            detail="Charging session not found",
        )

    db.delete(session)
    db.commit()

    return {"message": "Charging session deleted successfully"}
