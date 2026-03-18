from __future__ import annotations

from dataclasses import dataclass

from ..config import GeometryConfig, SymmetryConfig


@dataclass(frozen=True)
class SymmetrySpec:
    kind: str
    invariants: tuple[str, ...]
    equivariances: tuple[str, ...]


def resolve_symmetry(geometry: GeometryConfig, symmetry: SymmetryConfig) -> SymmetrySpec:
    if symmetry.kind:
        kind = symmetry.kind
    elif geometry.kind == "grid":
        kind = "periodic_translation"
    elif geometry.kind == "graph":
        kind = "permutation_locality"
    elif geometry.kind == "equivariant":
        kind = "euclidean_equivariance"
    else:
        raise ValueError(f"unsupported geometry kind: {geometry.kind}")

    mapping = {
        "periodic_translation": SymmetrySpec(
            kind=kind,
            invariants=("mean_vorticity",),
            equivariances=("translation",),
        ),
        "permutation_locality": SymmetrySpec(
            kind=kind,
            invariants=("node_relabeling",),
            equivariances=("permutation", "locality"),
        ),
        "euclidean_equivariance": SymmetrySpec(
            kind=kind,
            invariants=("feature_norms",),
            equivariances=("translation", "rotation"),
        ),
    }
    if kind not in mapping:
        raise ValueError(f"unsupported symmetry kind: {kind}")
    return mapping[kind]
