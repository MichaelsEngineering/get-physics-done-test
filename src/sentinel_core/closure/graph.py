from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class GraphClosure:
    kind: str = "graph_residual_head"

    def predict(self, state: list[float]) -> list[float]:
        return [0.05 * value for value in state]
