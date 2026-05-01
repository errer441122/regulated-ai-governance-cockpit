from __future__ import annotations

from dataclasses import dataclass


@dataclass
class CalibrationReporter:
    bins: int = 10

    def build_bins(self, labels: list[int], probabilities: list[float]) -> list[dict[str, float | int]]:
        output: list[dict[str, float | int]] = []
        for index in range(self.bins):
            low = index / self.bins
            high = (index + 1) / self.bins
            selected = [
                (label, probability)
                for label, probability in zip(labels, probabilities)
                if (low <= probability < high) or (index == self.bins - 1 and probability == 1.0)
            ]
            if selected:
                observed = sum(label for label, _ in selected) / len(selected)
                average_probability = sum(probability for _, probability in selected) / len(selected)
            else:
                observed = 0.0
                average_probability = 0.0
            output.append(
                {
                    "bin": index + 1,
                    "probability_low": round(low, 2),
                    "probability_high": round(high, 2),
                    "rows": len(selected),
                    "average_probability": round(average_probability, 4),
                    "observed_rate": round(observed, 4),
                }
            )
        return output
