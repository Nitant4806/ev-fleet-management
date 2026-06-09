# test_metadata.py

from app.database import Base
from app.models.vehicle import Vehicle
from app.models.trip import Trip

print(Base.metadata.tables.keys())
