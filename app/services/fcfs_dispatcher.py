from app.models.vehicle import Vehicle
from app.models.trip import Trip
from app.models.charging_station import ChargingStation

from app.core.enums import (
    VehicleStatus,
    TripStatus,
)

from app.services.charging_dispatcher import (
    assign_vehicle_to_station,
)

from app.services.charging_target_service import (
    calculate_target_soc,
)
from app.services.backtest_tracker import (
    tracker,
)
from app.services.risk_monitor_service import (
    evaluate_vehicle_risk,
)


def run_fcfs_dispatcher(db):

    stations = db.query(ChargingStation).all()

    vehicles = (
        db.query(Vehicle)
        .filter(
            Vehicle.status.in_(
                [
                    VehicleStatus.AVAILABLE,
                    VehicleStatus.RETURNED,
                ]
            )
        )
        .order_by(Vehicle.id)
        .all()
    )

    dispatched = 0

    for vehicle in vehicles:

        trip = (
            db.query(Trip)
            .filter(
                Trip.vehicle_id == vehicle.id,
                Trip.status == TripStatus.PENDING,
            )
            .order_by(Trip.scheduled_start_at)
            .first()
        )

        if trip is None:
            continue

        risk = evaluate_vehicle_risk(
            vehicle=vehicle,
            trip=trip,
        )

        if risk["deficit"] <= 0:
            continue

        station = None

        for s in stations:

            if s.available_chargers > 0:

                station = s

                break

        if station is None:
            tracker.rejected_dispatches += 1
            continue

        target_soc = calculate_target_soc(risk["required_soc"])

        success = assign_vehicle_to_station(
            db=db,
            vehicle=vehicle,
            station=station,
            target_soc=target_soc,
        )

        if success:
            dispatched += 1

    return dispatched
