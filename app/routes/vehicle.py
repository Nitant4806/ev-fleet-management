from fastapi import APIRouter, Depends, HTTPException
from app.schemas import vehicle
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.vehicle import Vehicle
from app.schemas.vehicle import VehicleCreate, VehicleUpdate

router = APIRouter()


@router.post("/vehicles")
def create_vehicle(vehicle: VehicleCreate, db: Session = Depends(get_db)):
    new_vehicle = Vehicle(
        vehicle_number=vehicle.vehicle_number,
        model=vehicle.model,
        battery_capacity=vehicle.battery_capacity,
        current_soc=vehicle.current_soc,
        efficiency_kwh_per_km=vehicle.efficiency_kwh_per_km,
        status=vehicle.status,
        location_name=vehicle.location_name,
    )

    db.add(new_vehicle)
    db.commit()
    db.refresh(new_vehicle)

    return {
        "message": "Vehicle created successfully",
        "id": new_vehicle.id,
    }


@router.get("/vehicles")
def get_vehicles(db: Session = Depends(get_db)):
    vehicles = db.query(Vehicle).all()

    return vehicles


@router.get("/vehicles/{vehicle_id}")
def get_vehicle(vehicle_id: int, db: Session = Depends(get_db)):
    vehicle = db.query(Vehicle).filter(Vehicle.id == vehicle_id).first()

    if vehicle is None:
        raise HTTPException(status_code=404, detail="Vehicle not found")

    return vehicle


@router.put("/vehicles/{vehicle_id}")
def update_vehicle(
    vehicle_id: int, vehicle_data: VehicleUpdate, db: Session = Depends(get_db)
):
    vehicle = db.query(Vehicle).filter(Vehicle.id == vehicle_id).first()

    if vehicle is None:
        raise HTTPException(status_code=404, detail="Vehicle not found")

    for field, value in vehicle_data.dict(exclude_unset=True).items():
        setattr(vehicle, field, value)

    db.commit()
    db.refresh(vehicle)

    return {
        "message": "Vehicle updated successfully",
        "id": vehicle.id,
    }


@router.delete("/vehicles/{vehicle_id}")
def delete_vehicle(vehicle_id: int, db: Session = Depends(get_db)):
    vehicle = db.query(Vehicle).filter(Vehicle.id == vehicle_id).first()

    if vehicle is None:
        raise HTTPException(status_code=404, detail="Vehicle not found")

    db.delete(vehicle)
    db.commit()

    return {"message": "Vehicle deleted successfully"}
