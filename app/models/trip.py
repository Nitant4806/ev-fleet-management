from app.core.enums import TripStatus
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey

from datetime import datetime
from app.database import Base

from sqlalchemy import Enum as SAEnum


class Trip(Base):
    __tablename__ = "trips"

    id = Column(Integer, primary_key=True, index=True)

    vehicle_id = Column(Integer, ForeignKey("vehicles.id"), nullable=False)

    start_location = Column(String, nullable=False)

    destination = Column(String, nullable=False)

    distance_km = Column(Float, nullable=False)

    estimated_duration_minutes = Column(Integer, nullable=False)

    status = Column(
        SAEnum(TripStatus, values_callable=lambda obj: [e.value for e in obj]),
        nullable=False,
        default=TripStatus.PENDING,
    )

    created_at = Column(DateTime, default=datetime.utcnow)

    completed_at = Column(DateTime, nullable=True)
