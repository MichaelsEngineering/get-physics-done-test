from __future__ import annotations

from dataclasses import dataclass

from ..geometry.graph import GraphGeometryState


@dataclass(frozen=True)
class GraphOperator:
    family: str = "graph_autoregressive_message_passing"
    processor_steps: int = 2

    def forward(self, state: list[float], geometry: GraphGeometryState) -> list[float]:
        features = state[:]
        for _ in range(self.processor_steps):
            updated = [0.0 for _ in features]
            counts = [0 for _ in features]
            for src, dst in geometry.edge_index:
                updated[dst] += 0.5 * features[src]
                counts[dst] += 1
            features = [
                0.6 * features[index] + (updated[index] / counts[index] if counts[index] else 0.0)
                for index in range(len(features))
            ]
        return features
