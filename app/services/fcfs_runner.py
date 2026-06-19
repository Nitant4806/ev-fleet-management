from app.services.simulation_runner import (
    process_pending_trips,
    process_completed_trips,
)

from app.services.charging_session_runner import (
    process_charging_sessions,
)

from app.services.fcfs_dispatcher import (
    run_fcfs_dispatcher,
)


def run_fcfs_cycle(db):

    process_pending_trips(db)

    process_completed_trips(db)

    run_fcfs_dispatcher(db)

    process_charging_sessions(db)
