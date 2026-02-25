from __future__ import annotations

from dataclasses import dataclass

from src.models import ExecutionResult


@dataclass(frozen=True)
class ScoreWeights:
    quality: float = 0.6
    cost: float = 0.25
    safety: float = 0.15


class ScoringEngine:
    def __init__(self, weights: ScoreWeights | None = None) -> None:
        self.weights = weights or ScoreWeights()

    def score(self, result: ExecutionResult, quarantined: bool) -> float:
        quality = min(100.0, max(0.0, 60.0 + len(result.output) / 8.0))
        cost = max(0.0, 100.0 - (result.tokens_used / 100.0))
        safety = 0.0 if quarantined else 100.0
        weighted = (
            quality * self.weights.quality
            + cost * self.weights.cost
            + safety * self.weights.safety
        )
        return round(weighted, 2)
