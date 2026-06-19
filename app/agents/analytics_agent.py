from app.agents.tools import (
    get_fleet_summary,
    get_station_utilization,
)


def analytics_agent(
    db,
    question: str,
):

    return {
        "agent": "Analytics",
        "fleet": get_fleet_summary(db),
        "stations": get_station_utilization(db),
    }
