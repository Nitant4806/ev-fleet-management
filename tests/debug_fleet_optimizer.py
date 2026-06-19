from app.database import SessionLocal

from app.services.fleet_optimizer_service import (
    optimize_fleet_from_db,
)

db = SessionLocal()

results = optimize_fleet_from_db(db)

print(f"Total recommendations: {len(results)}")

for result in results[:10]:
    print(result)
