from app.services.simulation_clock import (
    get_simulated_time,
)


def assign_priority(
    risk_score: int,
) -> str:

    if risk_score >= 70:
        return "CRITICAL"

    if risk_score >= 40:
        return "HIGH"

    if risk_score >= 20:
        return "MEDIUM"

    return "LOW"


def assign_action(
    recommendation: dict,
) -> str:

    if not recommendation["feasible"]:

        return "Trip at risk - immediate intervention required"

    risk_score = recommendation["risk_score"]

    if risk_score >= 70:

        return "Send vehicle to charging station immediately"

    if risk_score >= 40:

        return "Charge vehicle within next 30 minutes"

    if risk_score >= 20:

        return "Monitor and schedule charging"

    return "No action required"


def build_priority_queue(
    recommendations: list[dict],
):

    queue = []

    for recommendation in recommendations:

        item = recommendation.copy()

        item["priority"] = assign_priority(recommendation["risk_score"])

        item["action"] = assign_action(recommendation)

        queue.append(item)

    queue.sort(
        key=lambda x: x["risk_score"],
        reverse=True,
    )

    return queue
