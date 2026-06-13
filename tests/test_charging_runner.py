from app.database import SessionLocal

from app.models.vehicle import Vehicle

from app.core.enums import (
    VehicleStatus,
)

from app.services.charging_session_runner import (
    process_charging_sessions,
)

db = SessionLocal()

vehicle = db.query(Vehicle).first()

vehicle.current_soc = 25

vehicle.status = VehicleStatus.CHARGING

db.commit()

print("Before:")
print(vehicle.current_soc)
print(vehicle.status)

process_charging_sessions(db)

db.refresh(vehicle)

print()
print("After:")
print(vehicle.current_soc)
print(vehicle.status)
