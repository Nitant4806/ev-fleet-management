from pydantic import BaseModel, Field


class TripCreate(BaseModel):
    vehicle_id: int

    start_location: str
    destination: str

    distance_km: float = Field(gt=0)

    estimated_duration_minutes: int = Field(gt=0)

    status: str = "pending"


class TripUpdate(BaseModel):
    vehicle_id: int

    start_location: str
    destination: str

    distance_km: float = Field(gt=0)

    estimated_duration_minutes: int = Field(gt=0)

    status: str
