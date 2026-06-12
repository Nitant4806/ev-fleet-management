from app.models.vehicle import Vehicle
from app.models.charging_station import ChargingStation
from app.services.location_service import (
    calculate_travel_time_minutes,
)

from app.services.simulation_clock import (
    get_simulated_time,
)


def calculate_charge_time_minutes(
    vehicle: Vehicle,
    station: ChargingStation,
    soc_needed: float,
) -> float:

    kwh_needed = (soc_needed / 100) * vehicle.battery_capacity

    hours_needed = kwh_needed / station.max_power_kw

    return round(
        hours_needed * 60,
        2,
    )


def calculate_total_station_delay(
    travel_time_minutes: float,
    queue_time_minutes: float,
    charge_time_minutes: float,
) -> float:

    return round(
        travel_time_minutes + queue_time_minutes + charge_time_minutes,
        2,
    )


def find_best_station(
    vehicle: Vehicle,
    stations: list[ChargingStation],
    soc_needed: float,
):

    best_station = None
    best_delay = float("inf")

    for station in stations:

        charge_time = calculate_charge_time_minutes(
            vehicle=vehicle,
            station=station,
            soc_needed=soc_needed,
        )

        travel_time = calculate_travel_time_minutes(
            vehicle.location_name,
            station.location_name,
        )

        total_delay = calculate_total_station_delay(
            travel_time_minutes=travel_time,
            queue_time_minutes=station.avg_queue_minutes,
            charge_time_minutes=charge_time,
        )

        if total_delay < best_delay:
            best_delay = total_delay
            best_station = station

    return {
        "station_name": best_station.name,
        "total_delay": round(best_delay, 2),
    }


def can_charge_in_time(
    minutes_until_departure: float,
    total_delay_minutes: float,
) -> bool:

    return total_delay_minutes <= minutes_until_departure


def evaluate_station_feasibility(
    vehicle,
    trip,
    station,
    soc_needed,
):

    charge_time = calculate_charge_time_minutes(
        vehicle=vehicle,
        station=station,
        soc_needed=soc_needed,
    )

    travel_time = calculate_travel_time_minutes(
        vehicle.location_name,
        station.location_name,
    )

    queue_time = station.avg_queue_minutes

    total_delay = calculate_total_station_delay(
        travel_time_minutes=travel_time,
        queue_time_minutes=queue_time,
        charge_time_minutes=charge_time,
    )

    minutes_until_departure = (
        trip.scheduled_start_at - get_simulated_time()
    ).total_seconds() / 60

    feasible = can_charge_in_time(
        minutes_until_departure=minutes_until_departure,
        total_delay_minutes=total_delay,
    )

    buffer = round(
        minutes_until_departure - total_delay,
        2,
    )

    return {
        "station_name": station.name,
        "travel_time": travel_time,
        "queue_time": queue_time,
        "charge_time": charge_time,
        "total_delay": total_delay,
        "minutes_until_departure": round(
            minutes_until_departure,
            2,
        ),
        "buffer": buffer,
        "feasible": feasible,
    }
