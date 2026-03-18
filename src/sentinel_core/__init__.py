"""Simulation core organized around geometry -> symmetry -> operator -> closure -> integrator."""

from .config import (
    ClosureConfig,
    GeometryConfig,
    IntegratorConfig,
    OperatorConfig,
    SymmetryConfig,
    TaskConfig,
    TrainingConfig,
)
from .core import (
    RolloutResult,
    SimulationTask,
    TrainingResult,
    build_task,
    run_rollout,
    train_closure,
)
from .reporting import describe_architecture, package_file_tree, theory_mapping

__all__ = [
    "ClosureConfig",
    "GeometryConfig",
    "IntegratorConfig",
    "OperatorConfig",
    "RolloutResult",
    "SimulationTask",
    "SymmetryConfig",
    "TaskConfig",
    "TrainingConfig",
    "TrainingResult",
    "build_task",
    "describe_architecture",
    "package_file_tree",
    "run_rollout",
    "theory_mapping",
    "train_closure",
]
