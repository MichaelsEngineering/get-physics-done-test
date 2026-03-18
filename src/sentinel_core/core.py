from __future__ import annotations

from dataclasses import dataclass

from .closure import EquivariantClosure, GraphClosure, GridClosure
from .config import TaskConfig, TrainingConfig
from .geometry import (
    EquivariantGeometryState,
    GraphGeometryState,
    GridGeometryState,
    build_equivariant_geometry,
    build_graph_geometry,
    build_grid_geometry,
)
from .geometry.grid import Grid
from .integrators import StructurePreservingIntegrator
from .operators import EquivariantOperator, GraphOperator, GridOperator
from .symmetry.resolver import SymmetrySpec, resolve_symmetry
from .training import summarize_dataset


@dataclass(frozen=True)
class OperatorSpec:
    family: str
    structure_bias: str


@dataclass
class SimulationTask:
    name: str
    geometry: GridGeometryState | GraphGeometryState | EquivariantGeometryState
    symmetry: SymmetrySpec
    operator_spec: OperatorSpec
    operator: GridOperator | GraphOperator | EquivariantOperator
    closure: GridClosure | GraphClosure | EquivariantClosure
    integrator: StructurePreservingIntegrator | None
    config: TaskConfig


@dataclass(frozen=True)
class RolloutResult:
    trajectory: list[Grid]
    diagnostics: dict[str, float]


@dataclass(frozen=True)
class TrainingResult:
    summary: dict[str, float]


def _resolve_operator(config: TaskConfig, symmetry: SymmetrySpec) -> OperatorSpec:
    requested = config.operator.family
    if config.geometry.kind == "grid":
        family = requested or "regular_grid_differential"
        if symmetry.kind != "periodic_translation":
            raise ValueError("grid geometry requires periodic_translation symmetry")
        if family != "regular_grid_differential":
            raise ValueError("grid geometry only supports the regular_grid_differential operator")
        return OperatorSpec(family=family, structure_bias="local_stencil_plus_residual")

    if config.geometry.kind == "graph":
        family = requested or "graph_autoregressive_message_passing"
        if symmetry.kind != "permutation_locality":
            raise ValueError("graph geometry requires permutation_locality symmetry")
        if family != "graph_autoregressive_message_passing":
            raise ValueError("graph geometry only supports graph_autoregressive_message_passing")
        return OperatorSpec(family=family, structure_bias="message_passing")

    if config.geometry.kind == "equivariant":
        family = requested or "euclidean_equivariant_operator"
        if symmetry.kind != "euclidean_equivariance":
            raise ValueError("equivariant geometry requires euclidean_equivariance symmetry")
        if family != "euclidean_equivariant_operator":
            raise ValueError("equivariant geometry only supports euclidean_equivariant_operator")
        return OperatorSpec(family=family, structure_bias="equivariant_tensor_maps")

    raise ValueError(f"unsupported geometry kind: {config.geometry.kind}")


def build_task(config: TaskConfig) -> SimulationTask:
    symmetry = resolve_symmetry(config.geometry, config.symmetry)
    operator_spec = _resolve_operator(config, symmetry)

    if config.geometry.kind == "grid":
        geometry = build_grid_geometry(config.geometry)
        return SimulationTask(
            name=config.name,
            geometry=geometry,
            symmetry=symmetry,
            operator_spec=operator_spec,
            operator=GridOperator(family=operator_spec.family, viscosity=config.operator.viscosity),
            closure=GridClosure(
                kind=config.closure.kind,
                history=config.closure.history,
                latent_width=config.closure.latent_width,
            ),
            integrator=StructurePreservingIntegrator(
                kind=config.integrator.kind,
                dt=config.integrator.dt,
                projection=config.integrator.projection,
                max_stable_dt=config.integrator.max_stable_dt,
            ),
            config=config,
        )

    if config.geometry.kind == "graph":
        graph_geometry = build_graph_geometry(config.geometry)
        return SimulationTask(
            name=config.name,
            geometry=graph_geometry,
            symmetry=symmetry,
            operator_spec=operator_spec,
            operator=GraphOperator(family=operator_spec.family),
            closure=GraphClosure(kind=config.closure.kind),
            integrator=None,
            config=config,
        )

    if config.geometry.kind == "equivariant":
        equivariant_geometry = build_equivariant_geometry(config.geometry)
        return SimulationTask(
            name=config.name,
            geometry=equivariant_geometry,
            symmetry=symmetry,
            operator_spec=operator_spec,
            operator=EquivariantOperator(family=operator_spec.family),
            closure=EquivariantClosure(kind=config.closure.kind),
            integrator=None,
            config=config,
        )

    raise ValueError(f"unsupported geometry kind: {config.geometry.kind}")


def _grid_energy(field: Grid) -> float:
    flat = [value for row in field for value in row]
    return sum(value * value for value in flat) / len(flat)


def _grid_enstrophy(field: Grid) -> float:
    flat = [abs(value) for row in field for value in row]
    return sum(flat) / len(flat)


def run_rollout(task: SimulationTask, steps: int) -> RolloutResult:
    if task.config.geometry.kind != "grid":
        raise ValueError("rollout is implemented only for the grid turbulence vertical slice")
    assert isinstance(task.geometry, GridGeometryState)
    assert isinstance(task.operator, GridOperator)
    assert isinstance(task.closure, GridClosure)
    assert isinstance(task.integrator, StructurePreservingIntegrator)

    from .problems.turbulence import make_turbulence_dataset

    history = make_turbulence_dataset(task.geometry, samples=max(task.closure.history, 2))
    trajectory = [history[-1]]
    baseline_energy = _grid_energy(history[-1])
    baseline_enstrophy = _grid_enstrophy(history[-1])

    for _ in range(steps):
        state = trajectory[-1]
        tendencies = task.operator.tendencies(state)
        correction = task.closure.predict(history[-task.closure.history :])
        updated = task.integrator.step(state, tendencies, correction)
        history.append(updated)
        trajectory.append(updated)

    final_energy = _grid_energy(trajectory[-1])
    final_enstrophy = _grid_enstrophy(trajectory[-1])
    diagnostics = {
        "energy": final_energy,
        "enstrophy": final_enstrophy,
        "energy_drift": abs(final_energy - baseline_energy),
        "enstrophy_drift": abs(final_enstrophy - baseline_enstrophy),
        "mean_value": sum(value for row in trajectory[-1] for value in row)
        / (len(trajectory[-1]) * len(trajectory[-1][0])),
    }
    return RolloutResult(trajectory=trajectory, diagnostics=diagnostics)


def train_closure(
    task: SimulationTask, dataset: list[Grid], config: TrainingConfig
) -> TrainingResult:
    if task.config.geometry.kind != "grid":
        raise ValueError("training stub is only implemented for grid tasks")
    summary = summarize_dataset(dataset, config.epochs, config.teacher_forcing_steps)
    return TrainingResult(
        summary={
            "epochs": float(summary.epochs),
            "teacher_forcing_steps": float(summary.teacher_forcing_steps),
            "mean_sequence_energy": float(summary.mean_sequence_energy),
        }
    )
