import time
import random
import threading
from datetime import datetime

class PaymentServiceSimulator:
    def __init__(self):
        self.running = True

        self.current_load = 0
        self.max_load = 100

 
        self.total_requests = 0
        self.failed_requests = 0

    def simulate_request(self):
        """
        Simulate a single payment request
        """

        self.current_load += 1

        start_time = time.time()

       
        base_latency = random.uniform(50, 150)  # ms

      
        load_factor = self.current_load / self.max_load
        latency = base_latency * (1 + load_factor * 3)

       
        time.sleep(latency / 1000)

        failure_probability = 0.02 + (load_factor * 0.2)

        is_failed = random.random() < failure_probability

    
        self.total_requests += 1
        if is_failed:
            self.failed_requests += 1

  
        self.current_load -= 1

        return {
            "timestamp": datetime.utcnow().isoformat(),
            "service": "payment-service",
            "latency_ms": round(latency, 2),
            "success": not is_failed,
            "current_load": self.current_load
        }

    def traffic_generator(self):
        """
        Continuously generate fake traffic
        """
        while self.running:
            # Requests per second simulation
            rps = random.randint(5, 20)

            threads = []
            for _ in range(rps):
                t = threading.Thread(target=self.simulate_request)
                t.start()
                threads.append(t)

            for t in threads:
                t.join()

            time.sleep(1)

    def metrics_emitter(self):
        """
        Emit aggregated metrics every second
        """
        while self.running:
            error_rate = (
                self.failed_requests / self.total_requests
                if self.total_requests > 0 else 0
            )

            cpu = min(90, self.current_load * 2 + random.uniform(5, 15))

            metrics = {
                "timestamp": datetime.utcnow().isoformat(),
                "service": "payment-service",
                "requests_total": self.total_requests,
                "error_rate": round(error_rate, 4),
                "current_load": self.current_load,
                "cpu": round(cpu, 2)
            }

            print(metrics) 

            time.sleep(1)

    def start(self):
        threading.Thread(target=self.traffic_generator, daemon=True).start()
        threading.Thread(target=self.metrics_emitter, daemon=True).start()

        while True:
            time.sleep(10)