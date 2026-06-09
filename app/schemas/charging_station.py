from pydantic import BaseModel, Field


class ChargingStationCreate(BaseModel):
    name: str
    location_name: str

    total_chargers: int = Field(gt=0)

    available_chargers: int = Field(ge=0)


class ChargingStationUpdate(BaseModel):
    name: str
    location_name: str

    total_chargers: int = Field(gt=0)

    available_chargers: int = Field(ge=0)