from app.services.location_service import (
    calculate_travel_time_minutes,
)


def test_travel_time():

    result = calculate_travel_time_minutes(
        "DAIICT",
        "Gift City",
    )

    assert result >= 0
