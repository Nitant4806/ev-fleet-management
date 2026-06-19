from app.models.vehicle import Vehicle
from app.core.enums import VehicleStatus
import random

EV_MODELS = [
    "Tata Nexon EV",
    "Tata Punch EV",
    "MG ZS EV",
    "Mahindra XUV400",
    "BYD Atto 3",
]

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


def seed_vehicles(db):

    for i in range(100):

        vehicle = Vehicle(
            vehicle_number=f"GJ18EV{1000+i}",
            model=random.choice(EV_MODELS),
            battery_capacity=random.choice([30, 35, 40, 45, 50]),
            current_soc=random.randint(10, 100),
            efficiency_kwh_per_km=round(random.uniform(0.12, 0.20), 2),
            status=VehicleStatus.AVAILABLE.value,
            location_name=random.choice(LOCATIONS),
        )

        db.add(vehicle)

    db.commit()