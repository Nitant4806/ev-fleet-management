from app.models.vehicle import Vehicle

from app.core.enums import (
    VehicleStatus,
)

SOC_PER_MINUTE = 2


def calculate_station_queue_time(
    db,
    station,
):

    charging_vehicles = (
        db.query(Vehicle)
        .filter(
            Vehicle.charging_station_id == station.id,
            Vehicle.status == VehicleStatus.CHARGING,
        )
        .all()
    )

    if not charging_vehicles:
        return 0

    completion_times = []

    for vehicle in charging_vehicles:

        if vehicle.target_soc is None:
            continue

        remaining_soc = vehicle.target_soc - vehicle.current_soc

        remaining_soc = max(
            0,
            remaining_soc,
        )

        minutes_left = remaining_soc / SOC_PER_MINUTE

        completion_times.append(minutes_left)

    if not completion_times:
        return 0

    return round(
        min(completion_times),
        2,
    )
