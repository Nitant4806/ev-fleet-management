from app.services.risk_monitor_service import (
    evaluate_vehicle_risk,
)

from app.services.station_service import (
    find_best_station,
    evaluate_station_feasibility,
)


def generate_charging_recommendation(
    db,
    vehicle,
    trip,
    stations,
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
        db=db,
        vehicle=vehicle,
        stations=stations,
        soc_needed=risk["deficit"],
    )

    if best_station_result["station_name"] is None:

        return {
            "vehicle_id": vehicle.id,
            "trip_id": trip.id,
            "risk_score": risk["risk_score"],
            "required_soc": risk["required_soc"],
            "projected_soc": risk["projected_soc"],
            "deficit": risk["deficit"],
            "best_station": None,
            "travel_time": None,
            "queue_time": None,
            "charge_time": None,
            "total_delay": None,
            "buffer": None,
            "feasible": False,
            "recommendation": "No station available",
        }

    best_station = next(
        station
        for station in stations
        if station.name == best_station_result["station_name"]
    )

    feasibility = evaluate_station_feasibility(
        db=db,
        vehicle=vehicle,
        trip=trip,
        station=best_station,
        soc_needed=risk["deficit"],
    )

    recommendation = (
        "Dispatch immediately" if feasibility["feasible"] else "Trip at risk"
    )

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
