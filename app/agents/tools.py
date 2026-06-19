from app.models.vehicle import Vehicle
from app.models.charging_station import ChargingStation
from app.core.enums import (
    VehicleStatus,
)
from app.services.simulation_runner import (
    process_fleet_risks,
)

from app.services.fleet_priority_service import (
    build_priority_queue,
)
from app.services.simulation_runner import (
    process_fleet_risks,
)


def get_risky_vehicles(db):

    vehicles = db.query(Vehicle).filter(Vehicle.current_soc < 20).all()

    return [
        {
            "vehicle_number": v.vehicle_number,
            "soc": v.current_soc,
        }
        for v in vehicles
    ]


def get_station_utilization(db):

    stations = db.query(ChargingStation).all()

    return [
        {
            "station": s.name,
            "available": s.available_chargers,
            "total": s.total_chargers,
        }
        for s in stations
    ]


def get_critical_vehicles(db):

    vehicles = db.query(Vehicle).filter(Vehicle.current_soc < 20).all()

    return [
        {
            "vehicle_id": v.id,
            "vehicle_number": v.vehicle_number,
            "soc": v.current_soc,
            "status": str(v.status),
        }
        for v in vehicles
    ]


def get_fleet_summary(db):

    total = db.query(Vehicle).count()

    available = (
        db.query(Vehicle).filter(Vehicle.status == VehicleStatus.AVAILABLE).count()
    )

    charging = (
        db.query(Vehicle).filter(Vehicle.status == VehicleStatus.CHARGING).count()
    )

    on_trip = db.query(Vehicle).filter(Vehicle.status == VehicleStatus.ON_TRIP).count()

    returned = (
        db.query(Vehicle).filter(Vehicle.status == VehicleStatus.RETURNED).count()
    )

    return {
        "total_vehicles": total,
        "available": available,
        "charging": charging,
        "on_trip": on_trip,
        "returned": returned,
    }


def get_priority_queue(db):

    recommendations = process_fleet_risks(db)

    queue = build_priority_queue(recommendations)

    return queue[:10]


from app.models.vehicle import Vehicle


def explain_vehicle(
    db,
    vehicle_id: int,
):

    vehicle = db.query(Vehicle).filter(Vehicle.id == vehicle_id).first()

    if vehicle is None:

        return {"message": "Vehicle not found"}

    recommendations = process_fleet_risks(db)

    queue = build_priority_queue(recommendations)

    for item in queue:

        if item["vehicle_id"] == vehicle_id:

            return {
                "vehicle_id": item["vehicle_id"],
                "trip_id": item["trip_id"],
                "risk_score": item["risk_score"],
                "required_soc": item["required_soc"],
                "projected_soc": item["projected_soc"],
                "deficit": item["deficit"],
                "priority": item["priority"],
                "recommended_station": item["best_station"],
                "action": item["action"],
            }

    return {
        "vehicle_id": vehicle.id,
        "vehicle_number": vehicle.vehicle_number,
        "current_soc": vehicle.current_soc,
        "status": str(vehicle.status),
        "message": "Vehicle exists but is not currently in the optimizer queue",
    }
