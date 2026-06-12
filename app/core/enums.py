from enum import Enum


class VehicleStatus(str, Enum):
    AVAILABLE = "available"
    DISPATCHED = "dispatched"
    ON_TRIP = "on_trip"
    RETURNED = "returned"
    NEEDS_CHARGING = "needs_charging"
    CHARGING = "charging"
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
