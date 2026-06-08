from pydantic import BaseModel, Field
from app.core.enums import VehicleStatus


class VehicleCreate(BaseModel):
    vehicle_number: str
    model: str

    battery_capacity: float = Field(gt=0, description="Battery capacity in kWh")

    current_soc: float = Field(ge=0, le=100, description="State of charge percentage")

    efficiency_kwh_per_km: float = Field(gt=0, description="Energy consumption per km")

    status: VehicleStatus

    location_name: str

    class Config:
        from_attributes = True


from pydantic import BaseModel, Field
from app.core.enums import VehicleStatus


class VehicleUpdate(BaseModel):
    vehicle_number: str
    model: str

    battery_capacity: float = Field(gt=0)

    current_soc: float = Field(ge=0, le=100)

    efficiency_kwh_per_km: float = Field(gt=0)

    status: VehicleStatus

    location_name: str
