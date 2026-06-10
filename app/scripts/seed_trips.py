from app.database import SessionLocal
from app.models.vehicle import Vehicle
from app.models.trip import Trip
from app.core.enums import TripStatus

from datetime import datetime, timedelta

import random

db = SessionLocal()

vehicles = db.query(Vehicle).all()

LOCATIONS = [
    "Gift City",
    "DAIICT",
    "Infocity",
    "PDPU",
    "Raysan",
    "Kudasan",
    "Sector 21",
    "Sector 11",
    "Akshardham",
    "Gandhinagar Central",
]

for _ in range(500):

    vehicle = random.choice(vehicles)

    start_location = random.choice(LOCATIONS)

    destination = random.choice([loc for loc in LOCATIONS if loc != start_location])

    distance_km = round(random.uniform(2, 35), 2)

    trip = Trip(
        vehicle_id=vehicle.id,
        start_location=start_location,
        destination=destination,
        distance_km=distance_km,
        estimated_duration_minutes=int(distance_km * random.uniform(2, 4)),
        status=random.choice(
            [
                TripStatus.PENDING.value,
                TripStatus.IN_PROGRESS.value,
                TripStatus.COMPLETED.value,
            ]
        ),
        created_at=datetime.utcnow() - timedelta(days=random.randint(0, 30)),
    )

    db.add(trip)

db.commit()

print("500 trips inserted")
