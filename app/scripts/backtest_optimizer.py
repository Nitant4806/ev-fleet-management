from app.database import SessionLocal

from app.services.simulation_runner import (
    run_simulation_cycle,
)

from app.services.backtest_metrics import (
    BacktestMetrics,
)

from app.services.backtest_evaluator import (
    count_completed_trips,
    count_charging_vehicles,
    calculate_average_station_queue,
    calculate_utilization,
)
from app.services.backtest_tracker import (
    tracker,
)
from app.services.simulation_clock import (
    advance_simulation_time,
)
from app.models.trip import Trip
from app.core.enums import TripStatus

db = SessionLocal()

metrics = BacktestMetrics()
tracker.charging_sessions = 0
tracker.rejected_dispatches = 0

TOTAL_CYCLES = 200

print()
print("===== OPTIMIZER BACKTEST =====")
print()

for cycle in range(
    1,
    TOTAL_CYCLES + 1,
):

    run_simulation_cycle(db)

    advance_simulation_time(15)

    metrics.cycles += 1

    metrics.completed_trips = count_completed_trips(db)

    metrics.charging_sessions = tracker.charging_sessions

    metrics.total_queue_time += calculate_average_station_queue(db)

    utilization = calculate_utilization(db)

    metrics.total_utilization += utilization

    metrics.utilization_samples += 1

    if cycle % 20 == 0:

        print(f"Cycle {cycle} completed...")


pending_trips = db.query(Trip).filter(Trip.status == TripStatus.PENDING).count()

total_requests = tracker.charging_sessions + tracker.rejected_dispatches

success_rate = 0

if total_requests > 0:

    success_rate = round(
        (tracker.charging_sessions / total_requests) * 100,
        2,
    )

print()
print("===== RESULTS =====")
print()

print(
    "Cycles:",
    metrics.cycles,
)

print(
    "Completed Trips:",
    metrics.completed_trips,
)

print(
    "Pending Trips:",
    pending_trips,
)

print(
    "Charging Sessions:",
    metrics.charging_sessions,
)

print(
    "Rejected Dispatches:",
    tracker.rejected_dispatches,
)

print(
    "Average Queue Time:",
    metrics.average_queue_time(),
)

print(
    "Average Utilization:",
    metrics.average_utilization(),
    "%",
)

print(
    "Dispatch Success Rate:",
    success_rate,
    "%",
)
