def calculate_soc_drain(
    distance_km: float,
    efficiency_kwh_per_km: float,
    battery_capacity: float,
) -> float:

    kwh_used = distance_km * efficiency_kwh_per_km

    soc_drain = (kwh_used / battery_capacity) * 100

    return round(soc_drain, 2)


def apply_trip_to_vehicle(
    current_soc: float,
    distance_km: float,
    efficiency_kwh_per_km: float,
    battery_capacity: float,
) -> float:

    drain = calculate_soc_drain(
        distance_km,
        efficiency_kwh_per_km,
        battery_capacity,
    )

    new_soc = current_soc - drain

    return round(max(0, new_soc), 2)


from app.core.enums import VehicleStatus


def dispatch_vehicle(
    current_status: VehicleStatus,
) -> VehicleStatus:

    if current_status != VehicleStatus.AVAILABLE:
        raise ValueError("Only available vehicles can be dispatched")

    return VehicleStatus.DISPATCHED


def start_trip(
    current_status: VehicleStatus,
) -> VehicleStatus:

    if current_status != VehicleStatus.DISPATCHED:
        raise ValueError("Vehicle must be dispatched first")

    return VehicleStatus.ON_TRIP


def complete_trip(
    current_status: VehicleStatus,
) -> VehicleStatus:

    if current_status != VehicleStatus.ON_TRIP:
        raise ValueError("Vehicle is not on a trip")

    return VehicleStatus.RETURNED


from app.models.vehicle import Vehicle
from app.models.trip import Trip


def simulate_trip(
    vehicle: Vehicle,
    trip: Trip,
):

    vehicle.status = dispatch_vehicle(vehicle.status)

    vehicle.status = start_trip(vehicle.status)

    vehicle.current_soc = apply_trip_to_vehicle(
        current_soc=vehicle.current_soc,
        distance_km=trip.distance_km,
        efficiency_kwh_per_km=vehicle.efficiency_kwh_per_km,
        battery_capacity=vehicle.battery_capacity,
    )

    vehicle.location_name = trip.destination

    vehicle.status = complete_trip(vehicle.status)

    return vehicle
