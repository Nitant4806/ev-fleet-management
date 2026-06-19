from app.database import SessionLocal

from app.models.vehicle import Vehicle

from app.core.enums import (
    VehicleStatus,
)


from app.services.simulation_runner import (
    run_simulation_cycle,
)

db = SessionLocal()

vehicle_id = 130

vehicle = db.query(Vehicle).filter(Vehicle.id == vehicle_id).first()

print()
print("===== START TEST =====")

for cycle in range(1, 15):

    print()
    print(f"===== CYCLE {cycle} =====")

    run_simulation_cycle(db)

    db.refresh(vehicle)

    print(
        "Vehicle:",
        vehicle.id,
    )

    print(
        "SOC:",
        vehicle.current_soc,
    )

    print(
        "Status:",
        vehicle.status,
    )

    print(
        "Charging Station:",
        vehicle.charging_station_id,
    )

    print(
        "Target SOC:",
        vehicle.target_soc,
    )

    if vehicle.status == VehicleStatus.AVAILABLE and vehicle.target_soc is None:
        print()
        print("Charging completed.")
        break

print()
print("===== END TEST =====")
