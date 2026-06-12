from app.models.vehicle import Vehicle
from app.models.trip import Trip
from app.models.charging_station import ChargingStation

from app.services.charging_optimizer_service import (
    generate_charging_recommendation,
)

from app.services.simulation_clock import (
    get_simulated_time,
)


def optimize_fleet(
    vehicles: list[Vehicle],
    trips: list[Trip],
    stations: list[ChargingStation],
):

    recommendations = []

    for vehicle in vehicles:

        vehicle_trip = None

        for trip in trips:

            if trip.vehicle_id == vehicle.id and trip.status == "pending":
                vehicle_trip = trip
                break

        if vehicle_trip is None:
            continue

        minutes_until_departure = (
            vehicle_trip.scheduled_start_at - get_simulated_time()
        ).total_seconds() / 60

        if minutes_until_departure <= 0:
            continue

        if minutes_until_departure > 360:
            continue

        recommendation = generate_charging_recommendation(
            vehicle=vehicle,
            trip=vehicle_trip,
            stations=stations,
        )

        recommendations.append(recommendation)

    recommendations.sort(
        key=lambda x: x["risk_score"],
        reverse=True,
    )

    return recommendations


def optimize_fleet_from_db(db):

    vehicles = db.query(Vehicle).all()

    trips = db.query(Trip).filter(Trip.status == "pending").all()

    stations = db.query(ChargingStation).all()

    return optimize_fleet(
        vehicles=vehicles,
        trips=trips,
        stations=stations,
    )
