from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class GeometryConfig:
    kind: str
    resolution: int = 16
    domain_size: float = 6.283185307179586
    channels: tuple[str, ...] = ("vorticity",)
    boundary: str = "periodic"
    metadata: dict[str, str] = field(default_factory=dict)


@dataclass(frozen=True)
class SymmetryConfig:
    kind: str | None = None
    metadata: dict[str, str] = field(default_factory=dict)


@dataclass(frozen=True)
class OperatorConfig:
    family: str | None = None
    viscosity: float = 0.02
    metadata: dict[str, str] = field(default_factory=dict)


@dataclass(frozen=True)
class ClosureConfig:
    kind: str = "neural_operator_surrogate"
    history: int = 2
    latent_width: int = 8
    metadata: dict[str, str] = field(default_factory=dict)


@dataclass(frozen=True)
class IntegratorConfig:
    kind: str = "structure_preserving_euler"
    dt: float = 0.05
    projection: str = "mean_free"
    max_stable_dt: float = 0.1
    metadata: dict[str, str] = field(default_factory=dict)


@dataclass(frozen=True)
class TrainingConfig:
    epochs: int = 2
    learning_rate: float = 1e-3
    teacher_forcing_steps: int = 2


@dataclass(frozen=True)
class TaskConfig:
    name: str
    geometry: GeometryConfig
    symmetry: SymmetryConfig = field(default_factory=SymmetryConfig)
    operator: OperatorConfig = field(default_factory=OperatorConfig)
    closure: ClosureConfig = field(default_factory=ClosureConfig)
    integrator: IntegratorConfig = field(default_factory=IntegratorConfig)
