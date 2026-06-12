from datetime import datetime

from app.models.trip import Trip
from app.models.vehicle import Vehicle


SAFETY_BUFFER_SOC = 20


def calculate_required_soc(
    vehicle: Vehicle,
    trip: Trip,
) -> float:

    required_kwh = (
        trip.distance_km
        * vehicle.efficiency_kwh_per_km
    )

    required_soc = (
        required_kwh
        / vehicle.battery_capacity
    ) * 100

    return round(
        required_soc + SAFETY_BUFFER_SOC,
        2,
    )


def projected_soc_at_departure(
    current_soc: float,
    drain_rate_per_hour: float,
    scheduled_start_at: datetime,
) -> float:

    hours_until_departure = max(
        0,
        (
            scheduled_start_at
            - datetime.utcnow()
        ).total_seconds()
        / 3600,
    )

    projected_soc = (
        current_soc
        - (
            drain_rate_per_hour
            * hours_until_departure
        )
    )

    return round(
        max(0, projected_soc),
        2,
    )


def calculate_soc_deficit(
    required_soc: float,
    projected_soc: float,
) -> float:

    return round(
        max(
            0,
            required_soc - projected_soc,
        ),
        2,
    )


def calculate_risk_score(
    deficit: float,
) -> int:

    score = min(
        100,
        int((deficit / 30) * 100),
    )

    return score


def evaluate_vehicle_risk(
    vehicle: Vehicle,
    trip: Trip,
    drain_rate_per_hour: float,
) -> dict:

    required_soc = calculate_required_soc(
        vehicle,
        trip,
    )

    projected_soc = projected_soc_at_departure(
        current_soc=vehicle.current_soc,
        drain_rate_per_hour=drain_rate_per_hour,
        scheduled_start_at=trip.scheduled_start_at,
    )

    deficit = calculate_soc_deficit(
        required_soc,
        projected_soc,
    )

    risk_score = calculate_risk_score(
        deficit,
    )

    return {
        "vehicle_id": vehicle.id,
        "trip_id": trip.id,
        "required_soc": required_soc,
        "projected_soc": projected_soc,
        "deficit": deficit,
        "risk_score": risk_score,
        "at_risk": risk_score >= 70,
    }