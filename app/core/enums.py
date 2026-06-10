from enum import Enum


class VehicleStatus(str, Enum):
    AVAILABLE = "available"
    CHARGING = "charging"
    ON_TRIP = "on_trip"
    MAINTENANCE = "maintenance"
    OFFLINE = "offline"


class TripStatus(str, Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class ChargingSessionStatus(str, Enum):
    SCHEDULED = "scheduled"
    CHARGING = "charging"
    COMPLETED = "completed"
    CANCELLED = "cancelled"
