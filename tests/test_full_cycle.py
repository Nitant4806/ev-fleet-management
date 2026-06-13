from app.database import SessionLocal

from app.models.vehicle import Vehicle

from app.core.enums import (
    VehicleStatus,
)

from app.services.simulation_runner import (
    run_simulation_cycle,
)

db = SessionLocal()

vehicle = (
    db.query(Vehicle)
    .filter(
        Vehicle.id == 127
    )
    .first()
)

vehicle.current_soc = 15

vehicle.status = (
    VehicleStatus.AVAILABLE
)

vehicle.charging_station_id = None

db.commit()

print()
print("===== START TEST =====")

for cycle in range(1, 10):

    print()
    print(f"===== CYCLE {cycle} =====")

    queue = run_simulation_cycle(db)

    db.refresh(vehicle)

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

    if queue:

        print(
            "Top Priority:",
            queue[0]["vehicle_id"],
            queue[0]["priority"],
        )

    if vehicle.status == VehicleStatus.AVAILABLE:

        print()
        print(
            "Vehicle became AVAILABLE again."
        )

        break

print()
print("===== END TEST =====")