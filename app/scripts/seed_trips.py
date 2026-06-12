from app.database import SessionLocal
from app.models.vehicle import Vehicle
from app.models.trip import Trip
from app.core.enums import TripStatus

from datetime import datetime, timedelta

import random

db = SessionLocal()

# Prevent duplicate seeding
if db.query(Trip).count() > 0:
    print("Trips already exist")
    exit()

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

    distance_km = round(
        random.uniform(2, 35),
        2,
    )

    estimated_duration_minutes = int(distance_km * random.uniform(2.5, 3.5))

    # Rush-hour weighted scheduling
    hour = random.choices(
        population=[
            8,  # morning rush
            9,
            18,  # evening rush
            19,
            12,  # normal traffic
        ],
        weights=[
            25,
            20,
            25,
            20,
            10,
        ],
        k=1,
    )[0]

    day_offset = random.randint(0, 7)

    scheduled_start_at = (datetime.utcnow() + timedelta(days=day_offset)).replace(
        hour=hour,
        minute=random.randint(0, 59),
        second=0,
        microsecond=0,
    )

    expected_end_at = scheduled_start_at + timedelta(minutes=estimated_duration_minutes)

    trip = Trip(
        vehicle_id=vehicle.id,
        start_location=start_location,
        destination=destination,
        distance_km=distance_km,
        estimated_duration_minutes=estimated_duration_minutes,
        status=TripStatus.PENDING.value,
        created_at=datetime.utcnow(),
        scheduled_start_at=scheduled_start_at,
        started_at=None,
        expected_end_at=expected_end_at,
        completed_at=None,
    )

    db.add(trip)

db.commit()

print("500 trips inserted")
