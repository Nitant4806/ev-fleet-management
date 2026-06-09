from sqlalchemy import Column, Integer, String, DateTime, CheckConstraint

from datetime import datetime

from app.database import Base


class ChargingStation(Base):
    __tablename__ = "charging_stations"

    __table_args__ = (
        CheckConstraint(
            "available_chargers <= total_chargers", name="check_available_chargers"
        ),
    )

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String, nullable=False)

    location_name = Column(String, nullable=False)

    total_chargers = Column(Integer, nullable=False)

    available_chargers = Column(Integer, nullable=False)

    created_at = Column(DateTime, default=datetime.utcnow)

    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
