from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey

from datetime import datetime

from app.database import Base


class Trip(Base):
    __tablename__ = "trips"

    id = Column(Integer, primary_key=True, index=True)

    vehicle_id = Column(Integer, ForeignKey("vehicles.id"), nullable=False)

    start_location = Column(String, nullable=False)

    destination = Column(String, nullable=False)

    distance_km = Column(Float, nullable=False)

    estimated_duration_minutes = Column(Integer, nullable=False)

    status = Column(String, nullable=False, default="pending")

    created_at = Column(DateTime, default=datetime.utcnow)

    completed_at = Column(DateTime, nullable=True)
