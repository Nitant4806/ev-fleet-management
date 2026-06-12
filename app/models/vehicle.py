from sqlalchemy import Column, Integer, String, Float, DateTime, CheckConstraint

from datetime import datetime

from app.database import Base
from app.core.enums import VehicleStatus
from sqlalchemy import Enum as SAEnum


class Vehicle(Base):
    __tablename__ = "vehicles"

    __table_args__ = (
        CheckConstraint(
            "current_soc >= 0 AND current_soc <= 100", name="check_soc_range"
        ),
    )

    id = Column(Integer, primary_key=True, index=True)

    vehicle_number = Column(String, unique=True, nullable=False)

    model = Column(String, nullable=False)

    battery_capacity = Column(Float, nullable=False)

    current_soc = Column(Float, nullable=False)

    efficiency_kwh_per_km = Column(Float, nullable=False)

    status = Column(
        SAEnum(VehicleStatus, values_callable=lambda obj: [e.value for e in obj]),
        nullable=False,
        default=VehicleStatus.AVAILABLE,
    )
    location_name = Column(String, nullable=False)

    created_at = Column(DateTime, default=datetime.utcnow)

    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
