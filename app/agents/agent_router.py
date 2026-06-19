from app.agents.fleet_manager_agent import (
    fleet_manager_agent,
)

from app.agents.charging_advisor_agent import (
    charging_advisor_agent,
)

from app.agents.analytics_agent import (
    analytics_agent,
)
from app.agents.what_if_agent import (
    what_if_agent,
)


def route_agent(
    db,
    question: str,
):

    question = question.lower()

    if "critical" in question or "risk" in question or "attention" in question:

        return fleet_manager_agent(
            db,
            question,
        )

    if (
        "vehicle" in question
        or "selected" in question
        or "why" in question
        or "station" in question
        or "charge" in question
    ):
        return charging_advisor_agent(
            db,
            question,
        )

    if (
        "summary" in question
        or "summarize" in question
        or "health" in question
        or "analytics" in question
        or "congestion" in question
    ):
        return analytics_agent(
            db,
            question,
        )

    if "what if" in question:

        return what_if_agent(
            db,
            question,
        )

    return {"message": "Unknown question"}
