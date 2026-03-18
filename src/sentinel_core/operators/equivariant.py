from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class EquivariantOperator:
    family: str = "euclidean_equivariant_operator"

    def forward(
        self, scalars: list[float], vectors: list[tuple[float, float]]
    ) -> dict[str, object]:
        scaled_scalars = [1.1 * value for value in scalars]
        rotated_vectors = [(0.9 * x, 0.9 * y) for x, y in vectors]
        return {"scalars": scaled_scalars, "vectors": rotated_vectors}
