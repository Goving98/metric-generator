import random
import time
from concurrent.futures import ThreadPoolExecutor

class LoadEngine:
    def __init__(self, max_workers=50):
        self.executor = ThreadPoolExecutor(max_workers=max_workers)

    def generate_load(self, rps, task):
        futures = []
        for _ in range(rps):
            futures.append(self.executor.submit(task))
        return futures

    def shutdown(self):
        self.executor.shutdown(wait=True)