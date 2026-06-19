import asyncio

from app.services.websocket_manager import (
    manager,
)
from app.models.vehicle import Vehicle
from app.models.charging_station import ChargingStation

from app.services.charging_session_runner import (
    start_charging_session,
)

from app.services.backtest_tracker import (
    tracker,
)


from app.services.backtest_tracker import (
    tracker,
)
from app.services.event_service import (
    publish_event,
)


def assign_vehicle_to_station(
    db,
    vehicle,
    station,
    target_soc,
) -> bool:

    if station.available_chargers <= 0:

        tracker.rejected_dispatches += 1

        return False

    station.available_chargers -= 1

    tracker.charging_sessions += 1

    print(
        "SESSION COUNT:",
        tracker.charging_sessions,
    )

    vehicle.charging_station_id = station.id

    start_charging_session(
        vehicle=vehicle,
        station=station,
        target_soc=target_soc,
    )
    publish_event(
        {
            "event": "charging_started",
            "vehicle_id": vehicle.id,
            "station": station.name,
            "target_soc": target_soc,
        }
    )

    db.commit()

    return True
