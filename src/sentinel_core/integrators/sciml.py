from __future__ import annotations

from dataclasses import dataclass

from ..geometry.grid import Grid


@dataclass(frozen=True)
class StructurePreservingIntegrator:
    kind: str = "structure_preserving_euler"
    dt: float = 0.05
    projection: str = "mean_free"
    max_stable_dt: float = 0.1

    def validate(self) -> None:
        if self.dt <= 0:
            raise ValueError("integrator dt must be positive")
        if self.dt > self.max_stable_dt:
            raise ValueError("integrator dt exceeds configured stability bound")

    def step(self, field: Grid, tendencies: Grid, closure: Grid) -> Grid:
        self.validate()
        stepped = [
            [field[i][j] + self.dt * (tendencies[i][j] + closure[i][j]) for j in range(len(field))]
            for i in range(len(field))
        ]
        return self._project_mean_free(stepped) if self.projection == "mean_free" else stepped

    def _project_mean_free(self, field: Grid) -> Grid:
        flat = [value for row in field for value in row]
        mean = sum(flat) / len(flat)
        return [[value - mean for value in row] for row in field]
