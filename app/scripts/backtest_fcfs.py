from app.database import SessionLocal

from app.services.fcfs_dispatcher import (
    run_fcfs_dispatcher,
)

from app.services.charging_session_runner import (
    process_charging_sessions,
)

from app.services.backtest_tracker import (
    tracker,
)

from app.services.simulation_clock import (
    advance_simulation_time,
)
from app.services.fcfs_runner import (
    run_fcfs_cycle,
)

from app.models.trip import Trip

from app.core.enums import (
    TripStatus,
)

from app.services.backtest_evaluator import (
    calculate_utilization,
)

db = SessionLocal()

tracker.charging_sessions = 0
tracker.rejected_dispatches = 0

TOTAL_CYCLES = 200

for cycle in range(
    1,
    TOTAL_CYCLES + 1,
):

    run_fcfs_cycle(db)

    advance_simulation_time(15)

completed_trips = db.query(Trip).filter(Trip.status == TripStatus.COMPLETED).count()

pending_trips = db.query(Trip).filter(Trip.status == TripStatus.PENDING).count()

average_utilization = calculate_utilization(db)

print()
print("===== FCFS RESULTS =====")
print()

print(
    "Completed Trips:",
    completed_trips,
)

print(
    "Pending Trips:",
    pending_trips,
)

print(
    "Charging Sessions:",
    tracker.charging_sessions,
)

print(
    "Rejected Dispatches:",
    tracker.rejected_dispatches,
)

print(
    "Average Utilization:",
    average_utilization,
    "%",
)
