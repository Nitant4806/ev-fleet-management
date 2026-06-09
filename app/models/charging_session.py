from sqlalchemy import (
    Column,
    Integer,
    Float,
    String,
    DateTime,
    ForeignKey,
    CheckConstraint,
)

from datetime import datetime

from app.database import Base


class ChargingSession(Base):
    __tablename__ = "charging_sessions"

    __table_args__ = (
        CheckConstraint(
            "start_soc >= 0 AND start_soc <= 100",
            name="check_start_soc",
        ),
        CheckConstraint(
            "target_soc >= 0 AND target_soc <= 100",
            name="check_target_soc",
        ),
        CheckConstraint(
            "target_soc > start_soc",
            name="check_target_greater_than_start",
        ),
    )

    id = Column(
        Integer,
        primary_key=True,
        index=True,
    )

    vehicle_id = Column(
        Integer,
        ForeignKey("vehicles.id"),
        nullable=False,
    )

    station_id = Column(
        Integer,
        ForeignKey("charging_stations.id"),
        nullable=False,
    )

    start_soc = Column(
        Float,
        nullable=False,
    )

    target_soc = Column(
        Float,
        nullable=False,
    )

    status = Column(
        String,
        nullable=False,
        default="scheduled",
    )

    started_at = Column(
        DateTime,
        nullable=True,
    )

    ended_at = Column(
        DateTime,
        nullable=True,
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow,
    )
