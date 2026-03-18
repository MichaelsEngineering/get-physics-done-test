# Computational Architecture

**Analysis Date:** 2026-03-18

## Computational Pipeline

1. Define a `TaskConfig` with geometry, symmetry, operator, closure, and integrator settings
   - Script: `src/sentinel_core/config.py`
2. Build a `SimulationTask` through explicit geometry-to-operator resolution
   - Script: `src/sentinel_core/core.py`
3. Execute regular-grid rollout for the turbulence baseline
   - Script: `src/sentinel_core/core.py`
4. Surface diagnostics or scaffold reports through the CLI
   - Script: `src/gpd_test/cli.py`

## Key Algorithms

- Grid operator:
  local stencil Laplacian plus advection-like tendency surrogate
  - Implementation: `src/sentinel_core/operators/grid.py`
- Grid closure:
  history-aware local residual mixing used as a neuraloperator-oriented placeholder
  - Implementation: `src/sentinel_core/closure/grid.py`
- Structure-preserving integrator:
  explicit step plus mean-free projection and stability bound check
  - Implementation: `src/sentinel_core/integrators/sciml.py`
- Graph processor:
  encoder/processor/decoder-inspired message passing scaffold
  - Implementation: `src/sentinel_core/operators/graph.py`
- Equivariant operator:
  placeholder scalar/vector map preserving the representation distinction
  - Implementation: `src/sentinel_core/operators/equivariant.py`

## Data Flow

- Input config -> `build_task()` -> typed geometry/symmetry/operator/closure/integrator objects
- Grid task -> synthetic turbulence seed dataset -> rollout loop -> diagnostics dict
- CLI commands -> report or JSON summary -> human and automation consumption

## Performance and Reliability Concerns

- No large-scale numerics or GPU execution are present yet
- The key reliability surface is not throughput but physical failure modes under rollout
- Current bottlenecks are conceptual:
  missing plasma / MHD benchmark, missing horizon sweeps, missing transfer/regime protocols

## Libraries and Environment

- Local Python package with `typer`, `rich`, `pydantic`, `pyyaml`, `jinja2`
  - File: `pyproject.toml`
- Optional extras reserved for `sim`, `graph`, and `equivariant`
  - File: `pyproject.toml`

## Where Architecture Must Grow Next

- Add phase-2 benchmark harnesses around the existing grid rollout
- Add plasma / MHD state definitions without breaking the core task contract
- Add dedicated evaluation artifacts for transfer and regime shift rather than hiding them inside training stubs

---

_Architecture analysis: 2026-03-18_
