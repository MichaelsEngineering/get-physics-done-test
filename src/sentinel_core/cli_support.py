from __future__ import annotations

import json

from .config import GeometryConfig, TaskConfig, TrainingConfig
from .core import build_task, run_rollout, train_closure
from .geometry import EquivariantGeometryState, GraphGeometryState
from .operators import EquivariantOperator, GraphOperator
from .problems import default_grid_task_config
from .reporting import describe_architecture, package_file_tree, theory_mapping


def architecture_report() -> str:
    return describe_architecture()


def file_tree_report() -> str:
    return package_file_tree()


def theory_mapping_report() -> str:
    return theory_mapping()


def smoke_grid_report(steps: int = 3) -> str:
    task = build_task(default_grid_task_config())
    result = run_rollout(task, steps=steps)
    payload = {
        "task": task.name,
        "geometry": task.config.geometry.kind,
        "symmetry": task.symmetry.kind,
        "operator": task.operator_spec.family,
        "closure": task.config.closure.kind,
        "integrator": task.config.integrator.kind,
        "steps": steps,
        "diagnostics": result.diagnostics,
    }
    return json.dumps(payload, indent=2, sort_keys=True)


def training_report() -> str:
    task = build_task(default_grid_task_config())
    dataset = run_rollout(task, steps=1).trajectory[:2]
    result = train_closure(task, dataset=dataset, config=TrainingConfig())
    return json.dumps(result.summary, indent=2, sort_keys=True)


def graph_report() -> str:
    config = TaskConfig(name="graph_scaffold", geometry=GeometryConfig(kind="graph", resolution=6))
    task = build_task(config)
    assert isinstance(task.geometry, GraphGeometryState)
    assert isinstance(task.operator, GraphOperator)
    state = [float(index) for index in range(task.geometry.node_count)]
    propagated = task.operator.forward(state, task.geometry)
    return json.dumps(
        {
            "task": task.name,
            "symmetry": task.symmetry.kind,
            "operator": task.operator_spec.family,
            "output_norm": sum(abs(value) for value in propagated),
        },
        indent=2,
        sort_keys=True,
    )


def equivariant_report() -> str:
    config = TaskConfig(
        name="equivariant_scaffold", geometry=GeometryConfig(kind="equivariant", resolution=4)
    )
    task = build_task(config)
    assert isinstance(task.geometry, EquivariantGeometryState)
    assert isinstance(task.operator, EquivariantOperator)
    propagated = task.operator.forward([1.0, 2.0], [(1.0, 0.0), (0.0, 1.0)])
    scalars = propagated["scalars"]
    assert isinstance(scalars, list)
    return json.dumps(
        {
            "task": task.name,
            "symmetry": task.symmetry.kind,
            "operator": task.operator_spec.family,
            "feature_count": len(task.geometry.features),
            "scalar_sum": sum(scalars),
        },
        indent=2,
        sort_keys=True,
    )
