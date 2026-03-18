from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class EquivariantClosure:
    kind: str = "equivariant_residual_head"

    def predict(
        self, scalars: list[float], vectors: list[tuple[float, float]]
    ) -> dict[str, object]:
        return {
            "scalars": [0.02 * value for value in scalars],
            "vectors": [(0.02 * x, 0.02 * y) for x, y in vectors],
        }
