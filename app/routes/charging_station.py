from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.charging_station import ChargingStation
from app.schemas.charging_station import (
    ChargingStationCreate,
    ChargingStationUpdate,
)

router = APIRouter()


@router.post("/stations")
def create_station(
    station: ChargingStationCreate,
    db: Session = Depends(get_db)
):
    if station.available_chargers > station.total_chargers:
        raise HTTPException(
            status_code=400,
            detail="Available chargers cannot exceed total chargers"
        )

    new_station = ChargingStation(
        name=station.name,
        location_name=station.location_name,
        total_chargers=station.total_chargers,
        available_chargers=station.available_chargers,
    )

    db.add(new_station)
    db.commit()
    db.refresh(new_station)

    return {
        "message": "Charging station created successfully",
        "id": new_station.id,
    }


@router.get("/stations")
def get_stations(
    db: Session = Depends(get_db)
):
    return db.query(ChargingStation).all()


@router.get("/stations/{station_id}")
def get_station(
    station_id: int,
    db: Session = Depends(get_db)
):
    station = (
        db.query(ChargingStation)
        .filter(ChargingStation.id == station_id)
        .first()
    )

    if station is None:
        raise HTTPException(
            status_code=404,
            detail="Station not found"
        )

    return station


@router.put("/stations/{station_id}")
def update_station(
    station_id: int,
    station_data: ChargingStationUpdate,
    db: Session = Depends(get_db)
):
    station = (
        db.query(ChargingStation)
        .filter(ChargingStation.id == station_id)
        .first()
    )

    if station is None:
        raise HTTPException(
            status_code=404,
            detail="Station not found"
        )

    if (
        station_data.available_chargers
        > station_data.total_chargers
    ):
        raise HTTPException(
            status_code=400,
            detail="Available chargers cannot exceed total chargers"
        )

    for field, value in station_data.model_dump().items():
        setattr(station, field, value)

    db.commit()
    db.refresh(station)

    return {
        "message": "Station updated successfully",
        "id": station.id,
    }


@router.delete("/stations/{station_id}")
def delete_station(
    station_id: int,
    db: Session = Depends(get_db)
):
    station = (
        db.query(ChargingStation)
        .filter(ChargingStation.id == station_id)
        .first()
    )

    if station is None:
        raise HTTPException(
            status_code=404,
            detail="Station not found"
        )

    db.delete(station)
    db.commit()

    return {
        "message": "Station deleted successfully"
    }