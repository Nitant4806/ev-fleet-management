# create_tables.py

from app.database import engine, Base
from app.models.vehicle import Vehicle

Base.metadata.create_all(bind=engine)

print("✅ Tables created")
