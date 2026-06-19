from app.agents.tools import (
    explain_vehicle,
    get_priority_queue,
)


def charging_advisor_agent(
    db,
    question: str,
):

    question = question.lower()

    if "vehicle" in question:

        words = question.split()

        vehicle_id = None

        for word in words:

            if word.isdigit():

                vehicle_id = int(word)

                break

        if vehicle_id:

            return explain_vehicle(
                db,
                vehicle_id,
            )

    queue = get_priority_queue(db)

    if not queue:

        return {"message": "No charging needed"}

    return queue[0]
