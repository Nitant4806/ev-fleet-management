from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.trip import Trip
from app.models.vehicle import Vehicle
from app.schemas.trip import TripCreate, TripUpdate

router = APIRouter()


@router.post("/trips")
def create_trip(trip: TripCreate, db: Session = Depends(get_db)):
    vehicle = db.query(Vehicle).filter(Vehicle.id == trip.vehicle_id).first()

    if vehicle is None:
        raise HTTPException(status_code=404, detail="Vehicle not found")

    new_trip = Trip(
        vehicle_id=trip.vehicle_id,
        start_location=trip.start_location,
        destination=trip.destination,
        distance_km=trip.distance_km,
        estimated_duration_minutes=trip.estimated_duration_minutes,
        status=trip.status,
    )

    db.add(new_trip)
    db.commit()
    db.refresh(new_trip)

    return {
        "message": "Trip created successfully",
        "id": new_trip.id,
    }


@router.get("/trips")
def get_trips(db: Session = Depends(get_db)):
    trips = db.query(Trip).all()

    return trips


@router.get("/trips/{trip_id}")
def get_trip(trip_id: int, db: Session = Depends(get_db)):
    trip = db.query(Trip).filter(Trip.id == trip_id).first()

    if trip is None:
        raise HTTPException(status_code=404, detail="Trip not found")

    return trip


@router.put("/trips/{trip_id}")
def update_trip(trip_id: int, trip_data: TripUpdate, db: Session = Depends(get_db)):
    trip = db.query(Trip).filter(Trip.id == trip_id).first()

    if trip is None:
        raise HTTPException(status_code=404, detail="Trip not found")

    vehicle = db.query(Vehicle).filter(Vehicle.id == trip_data.vehicle_id).first()

    if vehicle is None:
        raise HTTPException(status_code=404, detail="Vehicle not found")

    for field, value in trip_data.model_dump().items():
        setattr(trip, field, value)

    db.commit()
    db.refresh(trip)

    return {
        "message": "Trip updated successfully",
        "id": trip.id,
    }


@router.delete("/trips/{trip_id}")
def delete_trip(trip_id: int, db: Session = Depends(get_db)):
    trip = db.query(Trip).filter(Trip.id == trip_id).first()

    if trip is None:
        raise HTTPException(status_code=404, detail="Trip not found")

    db.delete(trip)
    db.commit()

    return {"message": "Trip deleted successfully"}
