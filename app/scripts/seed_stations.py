from app.database import SessionLocal
from app.models.charging_station import ChargingStation

import random

db = SessionLocal()

stations = [
    ("Gift City Supercharger", "Gift City", 10),
    ("Infocity Charging Hub", "Infocity", 10),
    ("Gandhinagar Central Station", "Gandhinagar Central", 10),
    ("DAIICT Charging Point", "DAIICT", 6),
    ("PDPU Charging Center", "PDPU", 6),
    ("Raysan EV Station", "Raysan", 6),
    ("Kudasan EV Hub", "Kudasan", 6),
    ("Sector 21 EV Station", "Sector 21", 4),
    ("Sector 11 EV Station", "Sector 11", 4),
    ("Akshardham Charging Point", "Akshardham", 4),
]

for name, location, chargers in stations:

    station = ChargingStation(
        name=name,
        location_name=location,
        total_chargers=chargers,
        available_chargers=random.randint(0, chargers),
    )

    db.add(station)

db.commit()

print("10 stations inserted")
