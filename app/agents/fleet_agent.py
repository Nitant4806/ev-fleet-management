from app.agents.tools import (
    get_risky_vehicles,
    get_station_utilization,
    get_critical_vehicles,
    get_fleet_summary,
    get_priority_queue,
)


def ask_fleet_agent(
    db,
    question: str,
):

    question = question.lower()

    if "risky" in question or "risk" in question:

        return {"answer": get_risky_vehicles(db)}

    if "critical" in question:

        return {"answer": get_critical_vehicles(db)}

    if "station" in question or "utilization" in question:

        return {"answer": get_station_utilization(db)}

    if "summary" in question or "health" in question or "fleet" in question:

        return {"answer": get_fleet_summary(db)}

    if (
        "priority" in question
        or "charge next" in question
        or "what should charge next" in question
    ):

        return {"answer": get_priority_queue(db)}

    return {
        "answer": (
            "Try: risky vehicles, critical vehicles, "
            "fleet summary, station utilization, "
            "or what should charge next"
        )
    }
