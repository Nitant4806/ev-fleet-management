from app.database import SessionLocal

from app.services.simulation_runner import (
    run_simulation_cycle,
)

db = SessionLocal()

recommendations = run_simulation_cycle(db)

print(
    "Recommendations:",
    len(recommendations),
)

for recommendation in recommendations[:10]:

    print(recommendation)
