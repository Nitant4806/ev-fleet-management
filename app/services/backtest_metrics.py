class BacktestMetrics:

    def __init__(self):

        self.cycles = 0

        self.completed_trips = 0

        self.missed_trips = 0

        self.charging_sessions = 0

        self.total_queue_time = 0

        self.total_utilization = 0
        self.dispatch_success_rate = 0
        self.utilization_samples = 0
        self.rejected_dispatches = 0

    def average_queue_time(self):

        if self.cycles == 0:
            return 0

        return round(
            self.total_queue_time / self.cycles,
            2,
        )

    def average_utilization(self):

        if self.utilization_samples == 0:
            return 0

        return round(
            self.total_utilization / self.utilization_samples,
            2,
        )
