from app.database import SessionLocal

from app.models.vehicle import Vehicle

from app.core.enums import (
    VehicleStatus,
)

from app.services.simulation_runner import (
    process_fleet_risks,
)

from app.services.fleet_priority_service import (
    build_priority_queue,
)

db = SessionLocal()

vehicle = db.query(Vehicle).filter(Vehicle.id == 130).first()

vehicle.current_soc = 5

vehicle.status = VehicleStatus.RETURNED

vehicle.charging_station_id = None

db.commit()

recommendations = process_fleet_risks(db)

queue = build_priority_queue(recommendations)

print()

for item in queue:

    print(
        item["vehicle_id"],
        item["risk_score"],
        item["priority"],
        item["deficit"],
    )
