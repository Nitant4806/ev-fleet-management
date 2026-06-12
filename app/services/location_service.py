DISTANCES = {
    ("Gift City", "DAIICT"): 4,
    ("DAIICT", "Gift City"): 4,
    ("Gift City", "Infocity"): 3,
    ("Infocity", "Gift City"): 3,
    ("Gift City", "PDPU"): 6,
    ("PDPU", "Gift City"): 6,
    ("DAIICT", "Infocity"): 2,
    ("Infocity", "DAIICT"): 2,
    ("DAIICT", "PDPU"): 5,
    ("PDPU", "DAIICT"): 5,
    ("Gift City", "Gift City"): 0,
    ("DAIICT", "DAIICT"): 0,
    ("Infocity", "Infocity"): 0,
    ("PDPU", "PDPU"): 0,
}


def calculate_travel_time_minutes(
    source: str,
    destination: str,
) -> int:

    if source == destination:
        return 0

    distance = DISTANCES.get(
        (source, destination),
        5,
    )

    average_speed_kmph = 30

    return round((distance / average_speed_kmph) * 60)
