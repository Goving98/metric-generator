import random
import time
from core.metrics import RateTracker, LatencyTracker

class PaymentService:
    def __init__(self):
        self.total_requests = 0
        self.failed_requests = 0
        self.current_load = 0

        self.rate_tracker = RateTracker()
        self.latency_tracker = LatencyTracker()

        self.mode = "NORMAL"

    def set_mode(self, mode):
        self.mode = mode

    def process(self):
        self.current_load += 1

        base_latency = random.uniform(50, 120)

        # Mode behavior
        if self.mode == "SPIKE":
            base_latency *= 2
        elif self.mode == "DEGRADED":
            base_latency *= 3
        elif self.mode == "OUTAGE":
            base_latency *= 5

        latency = base_latency * (1 + self.current_load / 50)

        time.sleep(latency / 1000)

        # Failure probabilities
        failure_map = {
            "NORMAL": 0.02,
            "SPIKE": 0.05,
            "DEGRADED": 0.1,
            "OUTAGE": 0.4
        }

        failed = random.random() < failure_map[self.mode]

        self.total_requests += 1
        if failed:
            self.failed_requests += 1

        self.latency_tracker.add(latency)

        self.current_load -= 1

        return {
            "latency": latency,
            "failed": failed
        }

    def metrics(self):
        error_rate = self.failed_requests / self.total_requests if self.total_requests else 0

        return {
            "service": "payment-service",
            "rps": self.rate_tracker.calculate_rps(self.total_requests),
            "error_rate": round(error_rate, 4),
            "current_load": self.current_load,
            "latency": self.latency_tracker.percentiles(),
            "cpu": round(min(95, self.current_load * 2 + random.uniform(10, 20)), 2),
            "mode": self.mode
        }