from __future__ import annotations

from dataclasses import dataclass

from ..geometry.grid import Grid


@dataclass(frozen=True)
class GridOperator:
    family: str = "regular_grid_differential"
    viscosity: float = 0.02

    def laplacian(self, field: Grid) -> Grid:
        size = len(field)
        result: Grid = []
        for i in range(size):
            row: list[float] = []
            for j in range(size):
                center = field[i][j]
                north = field[(i - 1) % size][j]
                south = field[(i + 1) % size][j]
                west = field[i][(j - 1) % size]
                east = field[i][(j + 1) % size]
                row.append(north + south + west + east - 4.0 * center)
            result.append(row)
        return result

    def advect(self, field: Grid) -> Grid:
        size = len(field)
        result: Grid = []
        for i in range(size):
            row: list[float] = []
            for j in range(size):
                dx = 0.5 * (field[(i + 1) % size][j] - field[(i - 1) % size][j])
                dy = 0.5 * (field[i][(j + 1) % size] - field[i][(j - 1) % size])
                row.append(-(field[i][j] * dx + field[i][j] * dy))
            result.append(row)
        return result

    def tendencies(self, field: Grid) -> Grid:
        lap = self.laplacian(field)
        adv = self.advect(field)
        return [
            [adv[i][j] + self.viscosity * lap[i][j] for j in range(len(field))]
            for i in range(len(field))
        ]
