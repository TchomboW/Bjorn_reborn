import collections
import math
import logging

logger = logging.getLogger("bjorn_reborn.intel")

class StatisticsTracker:
    """
    Maintains a sliding window of observations to calculate 
    adaptive statistical thresholds (mu + k*sigma).
    """
    def __init__(self, window_size: int = 20):
        self.window_size = window_size
        self.history = collections.deque(maxlen=window_size)

    def add_observation(self, value: float):
        self.history.append(value)

    @property
    def mean(self) -> float:
        if not self.history:
            return 0.0
        return sum(self.history) / len(self.history)

    @property
    def std_dev(self) -> float:
        if len(self.history) < 2:
            return 0.0
        mean = self.mean
        variance = sum((x - mean) ** 2 for x in self.history) / len(self.history)
        return math.sqrt(variance)

    def is_anomaly(self, value: float, k: float = 3.0) -> bool:
        if len(self.history) < 5:  # Minimum samples for statistical significance
            return False
        mu = self.mean
        sigma = self.std_dev
        threshold = mu + (k * sigma)
        return value > threshold
