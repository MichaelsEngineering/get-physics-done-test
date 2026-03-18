from __future__ import annotations

import math

import pytest

from src.sentinel_core import (
    GeometryConfig,
    OperatorConfig,
    TaskConfig,
    TrainingConfig,
    build_task,
    run_rollout,
    theory_mapping,
    train_closure,
)
from src.sentinel_core.geometry import EquivariantGeometryState, GraphGeometryState
from src.sentinel_core.operators import EquivariantOperator, GraphOperator
from src.sentinel_core.problems import default_grid_task_config


def test_grid_chain_resolves_to_periodic_grid_operator() -> None:
    task = build_task(default_grid_task_config())

    assert task.symmetry.kind == "periodic_translation"
    assert task.operator_spec.family == "regular_grid_differential"
    assert task.config.closure.kind == "neural_operator_surrogate"
    assert task.integrator is not None


def test_invalid_operator_combination_fails_explicitly() -> None:
    config = TaskConfig(
        name="bad_grid_task",
        geometry=GeometryConfig(kind="grid"),
        operator=OperatorConfig(family="graph_autoregressive_message_passing"),
    )

    with pytest.raises(ValueError, match="regular_grid_differential"):
        build_task(config)


def test_grid_rollout_produces_finite_mean_free_state() -> None:
    task = build_task(default_grid_task_config(resolution=8))
    result = run_rollout(task, steps=3)

    assert len(result.trajectory) == 4
    assert result.diagnostics["energy"] > 0.0
    assert result.diagnostics["energy_drift"] < 5.0
    assert math.isfinite(result.diagnostics["enstrophy"])
    assert abs(result.diagnostics["mean_value"]) < 1e-9


def test_graph_scaffold_shares_same_build_path() -> None:
    config = TaskConfig(name="graph_task", geometry=GeometryConfig(kind="graph", resolution=6))
    task = build_task(config)
    assert isinstance(task.geometry, GraphGeometryState)
    assert isinstance(task.operator, GraphOperator)
    propagated = task.operator.forward([1.0] * task.geometry.node_count, task.geometry)

    assert task.symmetry.kind == "permutation_locality"
    assert len(propagated) == task.geometry.node_count


def test_equivariant_scaffold_exposes_euclidean_contract() -> None:
    config = TaskConfig(
        name="equivariant_task", geometry=GeometryConfig(kind="equivariant", resolution=4)
    )
    task = build_task(config)
    assert isinstance(task.geometry, EquivariantGeometryState)
    assert isinstance(task.operator, EquivariantOperator)
    propagated = task.operator.forward([1.0], [(1.0, 0.0)])
    vectors = propagated["vectors"]
    assert isinstance(vectors, list)

    assert task.symmetry.kind == "euclidean_equivariance"
    assert task.geometry.features[0].irrep_hint == "0e"
    assert vectors[0] == (0.9, 0.0)


def test_training_stub_returns_summary() -> None:
    task = build_task(default_grid_task_config(resolution=6))
    dataset = run_rollout(task, steps=1).trajectory[:2]
    result = train_closure(task, dataset, TrainingConfig())

    assert result.summary["epochs"] == 2.0
    assert result.summary["mean_sequence_energy"] > 0.0


def test_theory_mapping_mentions_bridge_components() -> None:
    text = theory_mapping()

    assert "Brandstetter" in text
    assert "SciML" in text
