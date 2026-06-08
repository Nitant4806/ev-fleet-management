from enum import Enum


class VehicleStatus(str, Enum):
    AVAILABLE = "available"
    CHARGING = "charging"
    ON_TRIP = "on_trip"
    MAINTENANCE = "maintenance"
    OFFLINE = "offline"
