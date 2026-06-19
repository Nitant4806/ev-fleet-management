from datetime import datetime, timedelta


class SimulationClock:

    def __init__(self):

        self.current_time = datetime.utcnow()

    def now(self):

        return self.current_time

    def advance_minutes(
        self,
        minutes: int,
    ):

        self.current_time += timedelta(minutes=minutes)

    def reset(self):

        self.current_time = datetime.utcnow()


simulation_clock = SimulationClock()


def get_simulated_time():

    return simulation_clock.now()


def advance_simulation_time(
    minutes: int,
):

    simulation_clock.advance_minutes(minutes)


def reset_simulation_time():

    simulation_clock.reset()
