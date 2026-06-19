from app.database import SessionLocal

from app.services.simulation_runner import (
    run_simulation_cycle,
)

from app.services.fcfs_dispatcher import (
    run_fcfs_dispatcher,
)

from app.services.backtest_tracker import (
    tracker,
)

db = SessionLocal()

print()
print("===== OPTIMIZER =====")

tracker.charging_sessions = 0
tracker.rejected_dispatches = 0

queue = run_simulation_cycle(db)

optimizer_sessions = tracker.charging_sessions

optimizer_rejected = tracker.rejected_dispatches

print(
    "Charging Sessions:",
    optimizer_sessions,
)

print(
    "Rejected Dispatches:",
    optimizer_rejected,
)

print()
print("===== FCFS =====")

tracker.charging_sessions = 0
tracker.rejected_dispatches = 0

fcfs_sessions = run_fcfs_dispatcher(db)

fcfs_rejected = tracker.rejected_dispatches

print(
    "Charging Sessions:",
    fcfs_sessions,
)

print(
    "Rejected Dispatches:",
    fcfs_rejected,
)

print()
print("===== COMPARISON =====")

print(
    "Optimizer Sessions:",
    optimizer_sessions,
)

print(
    "FCFS Sessions:",
    fcfs_sessions,
)

print(
    "Optimizer Rejected:",
    optimizer_rejected,
)

print(
    "FCFS Rejected:",
    fcfs_rejected,
)
