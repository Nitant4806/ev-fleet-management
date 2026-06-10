from app.database import SessionLocal
from app.models.vehicle import Vehicle
from app.models.charging_station import ChargingStation
from app.models.charging_session import ChargingSession
from app.core.enums import ChargingSessionStatus

from datetime import datetime, timedelta

import random

db = SessionLocal()

vehicles = db.query(Vehicle).all()
stations = db.query(ChargingStation).all()

for _ in range(200):

    vehicle = random.choice(vehicles)
    station = random.choice(stations)

    start_soc = random.randint(5, 40)

    session = ChargingSession(
        vehicle_id=vehicle.id,
        station_id=station.id,
        start_soc=start_soc,
        target_soc=random.randint(80, 100),
        status=ChargingSessionStatus.COMPLETED.value,
        started_at=datetime.utcnow() - timedelta(days=random.randint(1, 30)),
        ended_at=datetime.utcnow() - timedelta(days=random.randint(0, 1)),
    )

    db.add(session)

db.commit()

print("200 charging sessions inserted")
