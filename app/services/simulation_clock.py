from datetime import datetime, timedelta


class SimulationClock:

    SIMULATION_SPEED = 360

    def __init__(self):

        self.start_real_time = datetime.utcnow()

        self.start_sim_time = datetime.utcnow()

    def now(self):

        elapsed_real_seconds = (
            datetime.utcnow() - self.start_real_time
        ).total_seconds()

        elapsed_sim_seconds = elapsed_real_seconds * self.SIMULATION_SPEED

        return self.start_sim_time + timedelta(seconds=elapsed_sim_seconds)


simulation_clock = SimulationClock()


def get_simulated_time():

    return simulation_clock.now()
