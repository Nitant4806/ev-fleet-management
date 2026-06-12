from time import sleep

from app.services.simulation_clock import (
    SimulationClock,
)

clock = SimulationClock()

for _ in range(5):

    print(clock.now())

    sleep(1)
