# src/utils/zscore.py

class ZScoreTracker:
    def __init__(self, window_size=48):
        self.window_size = window_size
        self.values = []

    def update(self, new_value):
        self.values.append(new_value)
        if len(self.values) > self.window_size:
            self.values.pop(0)

        if len(self.values) < 2:
            return 0

        mean = sum(self.values) / len(self.values)
        variance = sum((x - mean) ** 2 for x in self.values) / len(self.values)
        std = variance ** 0.5

        if std == 0:
            return 0
        return (new_value - mean) / std
