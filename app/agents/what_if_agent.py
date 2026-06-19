from app.models.vehicle import Vehicle

from app.services.simulation_runner import (
    process_fleet_risks,
)

from app.services.fleet_priority_service import (
    build_priority_queue,
)


def what_if_agent(
    db,
    question: str,
):

    vehicles = db.query(Vehicle).all()

    low_soc_count = 0

    for vehicle in vehicles:

        if vehicle.current_soc < 20:

            low_soc_count += 1

    recommendations = process_fleet_risks(db)

    queue = build_priority_queue(recommendations)

    return {
        "agent": "What-If Agent",
        "scenario": question,
        "vehicles_below_20_soc": low_soc_count,
        "current_priority_count": len(queue),
        "estimated_dispatches": len(
            [
                item
                for item in queue
                if item["priority"]
                in [
                    "HIGH",
                    "CRITICAL",
                ]
            ]
        ),
        "recommendation": "Add chargers if critical queue continues growing.",
    }
