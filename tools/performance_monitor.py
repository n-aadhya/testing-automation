import psutil
import time


class PerformanceMonitor:

    def __init__(self):
        self.start_time = time.time()

    def get_metrics(self):
        cpu = psutil.cpu_percent(interval=0.5)
        memory = psutil.virtual_memory().percent

        return {
            "cpu": cpu,
            "memory": memory,
            "time": round(time.time() - self.start_time, 2)
        }
