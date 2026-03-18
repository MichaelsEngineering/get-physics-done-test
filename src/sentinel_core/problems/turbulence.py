from __future__ import annotations

from ..config import ClosureConfig, GeometryConfig, IntegratorConfig, OperatorConfig, TaskConfig
from ..geometry.grid import GridGeometryState, make_turbulence_seed


def default_grid_task_config(resolution: int = 12) -> TaskConfig:
    return TaskConfig(
        name="grid_turbulence",
        geometry=GeometryConfig(
            kind="grid", resolution=resolution, channels=("vorticity", "velocity")
        ),
        operator=OperatorConfig(family="regular_grid_differential", viscosity=0.03),
        closure=ClosureConfig(kind="neural_operator_surrogate", history=2, latent_width=16),
        integrator=IntegratorConfig(kind="structure_preserving_euler", dt=0.04, max_stable_dt=0.08),
    )


def make_turbulence_dataset(state: GridGeometryState, samples: int = 4) -> list[list[list[float]]]:
    return [make_turbulence_seed(state, phase=0.2 * sample) for sample in range(samples)]
