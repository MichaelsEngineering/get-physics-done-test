from __future__ import annotations

from dataclasses import dataclass

from ..config import GeometryConfig


@dataclass(frozen=True)
class EquivariantFeatureSpec:
    name: str
    irrep_hint: str


@dataclass(frozen=True)
class EquivariantGeometryState:
    kind: str
    dimension: int
    features: tuple[EquivariantFeatureSpec, ...]
    conserved_quantities: tuple[str, ...]


def build_equivariant_geometry(config: GeometryConfig) -> EquivariantGeometryState:
    return EquivariantGeometryState(
        kind=config.kind,
        dimension=2,
        features=(
            EquivariantFeatureSpec("scalar_density", "0e"),
            EquivariantFeatureSpec("vector_flux", "1o"),
        ),
        conserved_quantities=("norm",),
    )
