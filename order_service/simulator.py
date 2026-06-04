import random
import time
from core.metrics import RateTracker, LatencyTracker

class OrderService:
    def __init__(self, payment_service):
        self.payment_service = payment_service

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

        payment_result = self.payment_service.process()

        base_latency = random.uniform(30, 80)

        if self.mode == "SPIKE":
            base_latency *= 1.5
        elif self.mode == "DEGRADED":
            base_latency *= 2
        elif self.mode == "OUTAGE":
            base_latency *= 3

        latency = base_latency + payment_result["latency"]

        time.sleep(base_latency / 1000)

        failed = payment_result["failed"] or (random.random() < 0.02)

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
            "service": "order-service",
            "rps": self.rate_tracker.calculate_rps(self.total_requests),
            "error_rate": round(error_rate, 4),
            "current_load": self.current_load,
            "latency": self.latency_tracker.percentiles(),
            "cpu": round(min(95, self.current_load * 2 + random.uniform(5, 15)), 2),
            "mode": self.mode
        }