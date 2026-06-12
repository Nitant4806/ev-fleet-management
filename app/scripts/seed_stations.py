from app.database import SessionLocal
from app.models.charging_station import ChargingStation

import random

db = SessionLocal()

if db.query(ChargingStation).count() > 0:
    print("Stations already exist")
    exit()

stations = [
    (
        "Gift City Supercharger",
        "Gift City",
        10,
        120,
        5,
    ),
    (
        "Infocity Charging Hub",
        "Infocity",
        10,
        90,
        10,
    ),
    (
        "Gandhinagar Central Station",
        "Gandhinagar Central",
        10,
        60,
        15,
    ),
    (
        "DAIICT Charging Point",
        "DAIICT",
        6,
        30,
        20,
    ),
    (
        "PDPU Charging Center",
        "PDPU",
        6,
        60,
        10,
    ),
    (
        "Raysan EV Station",
        "Raysan",
        6,
        45,
        15,
    ),
    (
        "Kudasan EV Hub",
        "Kudasan",
        6,
        60,
        8,
    ),
    (
        "Sector 21 EV Station",
        "Sector 21",
        4,
        30,
        25,
    ),
    (
        "Sector 11 EV Station",
        "Sector 11",
        4,
        30,
        20,
    ),
    (
        "Akshardham Charging Point",
        "Akshardham",
        4,
        45,
        12,
    ),
]

for (
    name,
    location,
    chargers,
    max_power_kw,
    avg_queue_minutes,
) in stations:

    station = ChargingStation(
        name=name,
        location_name=location,
        total_chargers=chargers,
        available_chargers=random.randint(
            0,
            chargers,
        ),
        max_power_kw=max_power_kw,
        avg_queue_minutes=avg_queue_minutes,
    )

    db.add(station)

db.commit()

print("10 stations inserted")
