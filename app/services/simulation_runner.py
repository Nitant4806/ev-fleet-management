from datetime import timedelta

from app.models.vehicle import Vehicle
from app.models.trip import Trip
from app.models.charging_station import ChargingStation

from app.core.enums import (
    VehicleStatus,
    TripStatus,
)

from app.services.simulation_clock import (
    get_simulated_time,
)

from app.services.charging_optimizer_service import (
    generate_charging_recommendation,
)

from app.services.fleet_priority_service import (
    build_priority_queue,
)

from app.services.charging_dispatcher import (
    assign_vehicle_to_station,
)

from app.services.charging_session_runner import (
    process_charging_sessions,
)

from app.services.charging_target_service import (
    calculate_target_soc,
)
from app.services.backtest_tracker import (
    tracker,
)
from app.services.cache_service import (
    delete_cache,
)
from app.services.event_service import (
    publish_event,
)


def process_pending_trips(db):

    now = get_simulated_time()

    trips = db.query(Trip).filter(Trip.status == TripStatus.PENDING).all()

    for trip in trips:

        if trip.scheduled_start_at and trip.scheduled_start_at <= now:

            vehicle = db.query(Vehicle).filter(Vehicle.id == trip.vehicle_id).first()

            if vehicle.status != VehicleStatus.AVAILABLE:
                continue

            trip.status = TripStatus.IN_PROGRESS

            trip.started_at = now

            trip.expected_end_at = now + timedelta(
                minutes=trip.estimated_duration_minutes
            )

            vehicle.status = VehicleStatus.ON_TRIP
            publish_event(
                {
                    "event": "trip_started",
                    "vehicle_id": vehicle.id,
                }
            )

    db.commit()


def process_completed_trips(db):

    now = get_simulated_time()

    trips = db.query(Trip).filter(Trip.status == TripStatus.IN_PROGRESS).all()

    for trip in trips:

        if trip.expected_end_at and trip.expected_end_at <= now:

            vehicle = db.query(Vehicle).filter(Vehicle.id == trip.vehicle_id).first()

            trip.status = TripStatus.COMPLETED

            trip.completed_at = now

            vehicle.location_name = trip.destination

            soc_drain = (
                trip.distance_km
                * vehicle.efficiency_kwh_per_km
                / vehicle.battery_capacity
            ) * 100

            vehicle.current_soc -= soc_drain

            vehicle.current_soc = max(
                0,
                round(
                    vehicle.current_soc,
                    2,
                ),
            )

            vehicle.status = VehicleStatus.RETURNED

    db.commit()


def process_fleet_risks(db):

    vehicles = (
        db.query(Vehicle)
        .filter(
            Vehicle.status.in_(
                [
                    VehicleStatus.RETURNED,
                    VehicleStatus.AVAILABLE,
                ]
            )
        )
        .all()
    )

    pending_trips = db.query(Trip).filter(Trip.status == TripStatus.PENDING).count()

    stations = db.query(ChargingStation).all()

    recommendations = []

    for vehicle in vehicles:

        next_trip = (
            db.query(Trip)
            .filter(
                Trip.vehicle_id == vehicle.id,
                Trip.status == TripStatus.PENDING,
            )
            .order_by(Trip.scheduled_start_at)
            .first()
        )

        if next_trip is None:
            continue

        minutes_until_departure = (
            next_trip.scheduled_start_at - get_simulated_time()
        ).total_seconds() / 60

        print(
            f"Vehicle={vehicle.id}",
            f"Trip={next_trip.id}",
            f"Departure={next_trip.scheduled_start_at}",
            f"Now={get_simulated_time()}",
            f"Minutes={minutes_until_departure}",
        )

        if minutes_until_departure <= 0:
            print("SKIP -> departure passed")
            continue

        if minutes_until_departure > 1440:
            print("SKIP -> too far in future")
            continue

        recommendation = generate_charging_recommendation(
            db=db,
            vehicle=vehicle,
            trip=next_trip,
            stations=stations,
        )

        recommendations.append(recommendation)

    recommendations.sort(
        key=lambda x: x["risk_score"],
        reverse=True,
    )

    return recommendations


def run_simulation_cycle(db):

    process_pending_trips(db)

    process_completed_trips(db)

    recommendations = process_fleet_risks(db)

    priority_queue = build_priority_queue(recommendations)

    for item in priority_queue:

        if item["deficit"] <= 0:
            continue

        if item["priority"] not in [
            "HIGH",
            "CRITICAL",
        ]:
            continue

        if not item["best_station"]:
            continue

        vehicle = db.query(Vehicle).filter(Vehicle.id == item["vehicle_id"]).first()

        if vehicle is None:
            continue

        if vehicle.charging_station_id:
            continue

        if vehicle.status not in [
            VehicleStatus.AVAILABLE,
            VehicleStatus.RETURNED,
        ]:
            continue

        station = (
            db.query(ChargingStation)
            .filter(ChargingStation.name == item["best_station"])
            .first()
        )

        if station is None:
            continue

        if station.available_chargers <= 0:
            tracker.rejected_dispatches += 1
            continue

        target_soc = calculate_target_soc(item["required_soc"])

        assign_vehicle_to_station(
            db=db,
            vehicle=vehicle,
            station=station,
            target_soc=target_soc,
        )

    process_charging_sessions(db)

    delete_cache("fleet:analytics")
    delete_cache("stations:analytics")
    delete_cache("fleet:priorities")

    return priority_queue
