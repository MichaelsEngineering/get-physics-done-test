from __future__ import annotations

from dataclasses import dataclass

from ..geometry.grid import Grid


@dataclass(frozen=True)
class GridClosure:
    kind: str = "neural_operator_surrogate"
    history: int = 2
    latent_width: int = 8

    def predict(self, history: list[Grid]) -> Grid:
        latest = history[-1]
        previous = history[-2] if len(history) > 1 else latest
        size = len(latest)
        correction: Grid = []
        for i in range(size):
            row: list[float] = []
            for j in range(size):
                neighborhood = [
                    latest[i][j],
                    latest[(i - 1) % size][j],
                    latest[(i + 1) % size][j],
                    latest[i][(j - 1) % size],
                    latest[i][(j + 1) % size],
                ]
                local_mix = sum(neighborhood) / len(neighborhood)
                temporal = latest[i][j] - previous[i][j]
                row.append(0.12 * local_mix + 0.08 * temporal)
            correction.append(row)
        return correction
