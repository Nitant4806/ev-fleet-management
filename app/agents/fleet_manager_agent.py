from app.agents.tools import (
    get_priority_queue,
    get_fleet_summary,
)


def fleet_manager_agent(
    db,
    question: str,
):

    queue = get_priority_queue(db)

    summary = get_fleet_summary(db)

    return {
        "agent": "Fleet Manager",
        "fleet_summary": summary,
        "top_priorities": queue[:5],
    }
