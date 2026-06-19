from time import sleep

from app.services.simulation_clock import (
    get_simulated_time,
)

for _ in range(5):

    print(get_simulated_time())

    sleep(1)
