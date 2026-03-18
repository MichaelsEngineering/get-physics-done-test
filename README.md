# sentinel-multiscale-field-dynamics

This repository is a physics-first research program on multiscale turbulence and plasma dynamics, organized around the chain:

`geometry -> symmetry -> operator class -> closure -> integrator`

It combines a GPD-managed research map with a simulation-first Python package. The first executable vertical slice is periodic 2D grid turbulence with structure-preserving rollout diagnostics. GraphCast-inspired graph forecasting and e3nn-style equivariant states remain scaffold-level extensions on the same task interface.

## Research Program

The active program decomposes multiscale field dynamics into falsifiable subproblems across:

- Fluid turbulence
- Plasma / MHD
- Cross-scale surrogate modeling
- Invariant-preserving learned dynamics
- Long-horizon rollout stability
- Closure modeling for unresolved scales

Tracked failure modes:

- Energy drift
- Instability in long rollouts
- Failure across scale transfer
- Violation of conservation constraints
- Weakness under regime shift

## Sources Of Truth

- [PLAN.md](/home/qol/sentinel-multiscale-field-dynamics/PLAN.md) is the top-level program statement.
- [.gpd/PROJECT.md](/home/qol/sentinel-multiscale-field-dynamics/.gpd/PROJECT.md), [.gpd/REQUIREMENTS.md](/home/qol/sentinel-multiscale-field-dynamics/.gpd/REQUIREMENTS.md), and [.gpd/ROADMAP.md](/home/qol/sentinel-multiscale-field-dynamics/.gpd/ROADMAP.md) define the active GPD contract.
- [.gpd/research-map/PROJECT_MAP.md](/home/qol/sentinel-multiscale-field-dynamics/.gpd/research-map/PROJECT_MAP.md), [.gpd/research-map/VALIDATION.md](/home/qol/sentinel-multiscale-field-dynamics/.gpd/research-map/VALIDATION.md), and [.gpd/research-map/PAPER_OUTLINES.md](/home/qol/sentinel-multiscale-field-dynamics/.gpd/research-map/PAPER_OUTLINES.md) hold the current project map, verification strategy, and paper arcs.
- [docs/architecture.md](/home/qol/sentinel-multiscale-field-dynamics/docs/architecture.md) is the architecture report for the simulation package and theory mapping.

## Repository Layout

- `src/sentinel_core/` contains the simulation package and theory-chain abstractions.
- `src/scripts/` keeps the environment, recovery, and security tooling.
- `.gpd/` contains the active research-program state, requirements, roadmap, and research-map artifacts.
- `.codex/` contains vendored GPD workflows, references, and agent configuration.
- `paper_runs/` preserves earlier paper-production artifacts as historical context, not the active project contract.

## Working Model

- Geometry selects the state layout and conserved quantities.
- Symmetry is derived from geometry and constrains the admissible operator family.
- Operator class determines the numerical backbone and learned closure interface.
- Closure provides data-driven correction terms without bypassing the resolved dynamics.
- Integrator owns rollout stability and structure-preserving diagnostics.

## Install

```bash
uv sync --dev
uv sync --dev --extra sim
uv sync --dev --extra sim --extra graph --extra equivariant
```

## Workflow

Use repo-local tools. The expected local loop is:

```bash
make format
make check
```

For direct invocation, prefer `.venv` or `uv run` commands over assuming globally installed tools.

## Run

```bash
uv run gpd-test architecture
uv run gpd-test file-tree
uv run gpd-test smoke-grid
uv run gpd-test theory-mapping
.venv/bin/pytest -q
```

## Notes On Optional Stacks

- Base installs stay lightweight for GPD and repo-policy workflows.
- `sim` is the regular-grid operator-learning stack.
- `graph` is reserved for GraphCast-style graph/mesh experimentation.
- `equivariant` is reserved for e3nn-style Euclidean-equivariant modules.

## Referenced Software

```bibtex
@software{physical_superintelligence_2026_gpd,
  author = {{Physical Superintelligence PBC}},
  title = {Get Physics Done (GPD)},
  version = {1.1.0},
  year = {2026},
  url = {https://github.com/psi-oss/get-physics-done},
  license = {Apache-2.0}
}
```
