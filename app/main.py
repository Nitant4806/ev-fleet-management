from fastapi import FastAPI
from sqlalchemy import text
from app.database import get_db
from fastapi import Depends
from sqlalchemy.orm import Session
from app.routes.vehicle import router as vehicle_router
from app.routes.trip import router as trip_router
from app.routes.charging_station import (
    router as charging_station_router
)

app = FastAPI(
    title="EV Fleet Management API",
    version="1.0.0",
    description="Intelligent charging optimization for electric vehicle fleets",
)

app.include_router(charging_station_router)

app.include_router(vehicle_router)
app.include_router(trip_router)


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
