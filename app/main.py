from fastapi import FastAPI
from sqlalchemy import text
from app.database import get_db
from fastapi import Depends
from sqlalchemy.orm import Session
from app.routes.vehicle import router as vehicle_router
from app.routes.trip import router as trip_router
from app.routes.charging_station import router as charging_station_router
from app.routes.charging_session import router as charging_session_router
from app.models.user import User
from app.routes.auth import router as auth_router
from app.routes.user import router as user_router
from app.routes.simulation import (
    router as simulation_router,
)

from app.routes.fleet import (
    router as fleet_router,
)

from app.routes.stations import (
    router as stations_router,
)
from app.routes.analytics import (
    router as analytics_router,
)

app = FastAPI(
    title="EV Fleet Management API",
    version="1.0.0",
    description="Intelligent charging optimization for electric vehicle fleets",
)

app.include_router(charging_station_router)
app.include_router(vehicle_router)
app.include_router(trip_router)
app.include_router(charging_session_router)

app.include_router(auth_router)
app.include_router(user_router)

app.include_router(simulation_router)

app.include_router(fleet_router)

app.include_router(stations_router)
app.include_router(analytics_router)


@app.get("/")
def root():
    return {"message": "EV Fleet API is running", "version": "1.0.0"}


@app.get("/health")
def health(db: Session = Depends(get_db)):
    try:
        db.execute(text("SELECT 1"))
        return {"status": "ok", "database": "connected"}
    except Exception as e:
        return {"status": "error", "database": str(e)}
