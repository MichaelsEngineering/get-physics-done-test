from __future__ import annotations

from dataclasses import dataclass
from math import cos, pi, sin

from ..config import GeometryConfig

Grid = list[list[float]]


@dataclass(frozen=True)
class GridGeometryState:
    kind: str
    resolution: int
    domain_size: float
    boundary: str
    channels: tuple[str, ...]
    conserved_quantities: tuple[str, ...]
    coordinates: tuple[list[float], list[float]]


def build_grid_geometry(config: GeometryConfig) -> GridGeometryState:
    coords = [
        (config.domain_size * index) / config.resolution for index in range(config.resolution)
    ]
    return GridGeometryState(
        kind=config.kind,
        resolution=config.resolution,
        domain_size=config.domain_size,
        boundary=config.boundary,
        channels=config.channels,
        conserved_quantities=("energy", "enstrophy", "circulation"),
        coordinates=(coords, coords.copy()),
    )


def make_turbulence_seed(state: GridGeometryState, phase: float = 0.0) -> Grid:
    field: Grid = []
    scale = 2.0 * pi / state.domain_size
    for i, x in enumerate(state.coordinates[0]):
        row: list[float] = []
        for j, y in enumerate(state.coordinates[1]):
            mode = sin(scale * (x + phase)) * cos(scale * (y - phase))
            fine = 0.35 * sin(2.0 * scale * (x - y + phase))
            row.append(mode + fine + 0.05 * sin((i + j) * scale))
        field.append(row)
    return field
