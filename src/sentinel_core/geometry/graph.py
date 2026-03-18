from __future__ import annotations

from dataclasses import dataclass

from ..config import GeometryConfig


@dataclass(frozen=True)
class GraphGeometryState:
    kind: str
    node_count: int
    node_features: tuple[str, ...]
    edge_index: tuple[tuple[int, int], ...]
    conserved_quantities: tuple[str, ...]


def build_graph_geometry(config: GeometryConfig) -> GraphGeometryState:
    node_count = max(config.resolution, 4)
    edges: list[tuple[int, int]] = []
    for node in range(node_count):
        edges.append((node, (node + 1) % node_count))
        edges.append(((node + 1) % node_count, node))
    return GraphGeometryState(
        kind=config.kind,
        node_count=node_count,
        node_features=("state", "forcing"),
        edge_index=tuple(edges),
        conserved_quantities=("mass",),
    )
