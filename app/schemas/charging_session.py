from pydantic import BaseModel, Field


class ChargingSessionCreate(BaseModel):
    vehicle_id: int
    station_id: int

    start_soc: float = Field(ge=0, le=100)
    target_soc: float = Field(ge=0, le=100)

    status: str = "scheduled"


class ChargingSessionUpdate(BaseModel):
    vehicle_id: int
    station_id: int

    start_soc: float = Field(ge=0, le=100)
    target_soc: float = Field(ge=0, le=100)

    status: str
