import time
from collections import deque

class RateTracker:
    def __init__(self):
        self.last_total = 0
        self.last_time = time.time()

    def calculate_rps(self, current_total):
        now = time.time()
        elapsed = now - self.last_time

        if elapsed == 0:
            return 0

        rps = (current_total - self.last_total) / elapsed

        self.last_total = current_total
        self.last_time = now

        return round(rps, 2)


class LatencyTracker:
    def __init__(self, window_size=200):
        self.latencies = deque(maxlen=window_size)

    def add(self, latency):
        self.latencies.append(latency)

    def percentiles(self):
        if not self.latencies:
            return {"p50": 0, "p95": 0, "p99": 0}

        sorted_lat = sorted(self.latencies)
        n = len(sorted_lat)

        return {
            "p50": round(sorted_lat[int(0.5 * n)], 2),
            "p95": round(sorted_lat[int(0.95 * n) - 1], 2),
            "p99": round(sorted_lat[int(0.99 * n) - 1], 2),
        }