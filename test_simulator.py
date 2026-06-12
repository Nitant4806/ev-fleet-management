from app.services.simulator_service import apply_trip_to_vehicle

print(
    apply_trip_to_vehicle(
        current_soc=75,
        distance_km=20,
        efficiency_kwh_per_km=0.2,
        battery_capacity=40,
    )
)
