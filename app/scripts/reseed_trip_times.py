from datetime import timedelta
import random

from app.database import SessionLocal
from app.models.trip import Trip

from app.services.simulation_clock import (
    get_simulated_time,
)

db = SessionLocal()

now = get_simulated_time()

trips = db.query(Trip).all()

for trip in trips:

    trip.scheduled_start_at = now + timedelta(
        minutes=random.randint(
            30,
            1440,
        )
    )

db.commit()

print("Trip times reseeded")
