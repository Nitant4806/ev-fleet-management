from app.database import SessionLocal
from app.services.simulation_runner import (
    run_simulation_cycle,
)

db = SessionLocal()

queue = run_simulation_cycle(db)

print(
    "Priority Queue Size:",
    len(queue),
)

for item in queue[:10]:

    print()

    print("Vehicle:", item["vehicle_id"])

    print("Trip:", item["trip_id"])

    print("Risk:", item["risk_score"])

    print("Priority:", item["priority"])

    print("Action:", item["action"])

    print("Station:", item["best_station"])

    print("Buffer:", item["buffer"])
