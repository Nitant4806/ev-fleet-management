SAFETY_MARGIN = 5


def calculate_target_soc(
    required_soc: float,
) -> float:

    return min(
        100,
        round(
            required_soc + SAFETY_MARGIN,
            2,
        ),
    )
