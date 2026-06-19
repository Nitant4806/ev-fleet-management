from app.models.vehicle import Vehicle
from app.models.trip import Trip
from app.core.enums import TripStatus

from datetime import datetime, timedelta
import random


def seed_trips(db):

    if db.query(Trip).count() > 0:
        return

    vehicles = db.query(Vehicle).all()

    if not vehicles:
        return

    locations = [
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

        start_location = random.choice(locations)

        destination = random.choice(
            [
                loc
                for loc in locations
                if loc != start_location
            ]
        )

        distance_km = round(
            random.uniform(2, 35),
            2,
        )

        estimated_duration_minutes = int(
            distance_km * random.uniform(2.5, 3.5)
        )

        hour = random.choices(
            population=[8, 9, 18, 19, 12],
            weights=[25, 20, 25, 20, 10],
            k=1,
        )[0]

        day_offset = random.randint(
            0,
            1,  # keep trips within next 24 hours
        )

        scheduled_start_at = (
            datetime.utcnow()
            + timedelta(days=day_offset)
        ).replace(
            hour=hour,
            minute=random.randint(0, 59),
            second=0,
            microsecond=0,
        )

        expected_end_at = (
            scheduled_start_at
            + timedelta(
                minutes=estimated_duration_minutes
            )
        )

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