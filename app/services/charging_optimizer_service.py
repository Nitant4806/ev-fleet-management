from app.models.vehicle import Vehicle
from app.models.trip import Trip
from app.models.charging_station import ChargingStation

from app.services.risk_monitor_service import (
    evaluate_vehicle_risk,
)

from app.services.station_service import (
    find_best_station,
    evaluate_station_feasibility,
)


def generate_charging_recommendation(
    vehicle: Vehicle,
    trip: Trip,
    stations: list[ChargingStation],
    drain_rate_per_hour: float = 4,
) -> dict:

    risk = evaluate_vehicle_risk(
        vehicle=vehicle,
        trip=trip,
    )

    if risk["deficit"] == 0:

        return {
            "vehicle_id": vehicle.id,
            "trip_id": trip.id,
            "risk_score": 0,
            "required_soc": risk["required_soc"],
            "projected_soc": risk["projected_soc"],
            "deficit": 0,
            "best_station": None,
            "travel_time": 0,
            "queue_time": 0,
            "charge_time": 0,
            "total_delay": 0,
            "buffer": None,
            "feasible": True,
            "recommendation": "No charging required",
        }

    best_station_result = find_best_station(
        vehicle=vehicle,
        stations=stations,
        soc_needed=risk["deficit"],
    )

    best_station = next(
        station
        for station in stations
        if station.name == best_station_result["station_name"]
    )

    feasibility = evaluate_station_feasibility(
        vehicle=vehicle,
        trip=trip,
        station=best_station,
        soc_needed=risk["deficit"],
    )

    if feasibility["feasible"]:
        recommendation = "Dispatch immediately"
    else:
        recommendation = "Trip at risk"

    return {
        "vehicle_id": vehicle.id,
        "trip_id": trip.id,
        "risk_score": risk["risk_score"],
        "required_soc": risk["required_soc"],
        "projected_soc": risk["projected_soc"],
        "deficit": risk["deficit"],
        "best_station": feasibility["station_name"],
        "travel_time": feasibility["travel_time"],
        "queue_time": feasibility["queue_time"],
        "charge_time": feasibility["charge_time"],
        "total_delay": feasibility["total_delay"],
        "buffer": feasibility["buffer"],
        "feasible": feasibility["feasible"],
        "recommendation": recommendation,
    }
