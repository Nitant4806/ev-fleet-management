# test_db.py

from app.database import engine

try:
    with engine.connect() as conn:
        print("✅ Database Connected Successfully")
except Exception as e:
    print("❌ Error:", e)