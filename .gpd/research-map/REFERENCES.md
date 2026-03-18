# Reference and Anchor Map

**Analysis Date:** 2026-03-18

## Active Anchor Registry

| Anchor ID | Anchor | Type | Source / Locator | Why It Matters | Contract Subject IDs | Required Action | Carry Forward To |
| --------- | ------ | ---- | ---------------- | -------------- | -------------------- | --------------- | ---------------- |
| `Ref-program-plan` | Program plan | spec | `PLAN.md` | Defines domains, deliverables, and tracked failure modes | `claim-unification-program` | read, use | planning, writing |
| `Ref-project` | Project contract | spec | `.gpd/PROJECT.md` | Defines the research question, scope, anchors, and skeptical framing | `claim-unification-program` | read, align | planning, verification, writing |
| `Ref-architecture-report` | Architecture summary | doc | `docs/architecture.md` | States the program spine and theory mapping | `claim-unification-program` | read, cite, align | planning, verification, writing |
| `Ref-simulation-core` | Simulation package | code | `src/sentinel_core/` | Contains the executable baseline and extension surfaces | `SIM-01`, `SIM-03` | read, extend, compare | execution, verification |
| `Ref-grid-task` | Grid turbulence task | code | `src/sentinel_core/problems/turbulence.py` | Provides the first executable vertical slice | `SIM-01`, `SIM-02` | run, extend | execution, verification, writing |
| `Ref-rollout` | Rollout diagnostics | code | `src/sentinel_core/core.py` | Current home of energy/enstrophy drift and mean diagnostics | `SIM-02`, `VALD-02`, `VALD-03` | inspect, extend | execution, verification |
| `Ref-integrator` | Structure-preserving integrator | code | `src/sentinel_core/integrators/sciml.py` | Defines current stability and projection surface | `SIM-02`, `GEN-03` | inspect, extend | execution, verification |
| `Ref-tests` | Baseline tests | test | `tests/test_simulation_architecture.py` | Existing executable checks for compatibility and rollout sanity | `VALD-04` | run, extend | execution, verification |
| `Ref-cli` | CLI surface | tool | `src/gpd_test/cli.py` | Provides smoke-run and architecture-report entrypoints | `SIM-01`, `MAP-01` | use, extend | execution, writing |

## Benchmarks and Comparison Targets

- Rollout drift metrics on the grid turbulence baseline
  - Source: `src/sentinel_core/core.py`
  - Compared in: future Phase-2 benchmark artifacts
  - Status: baseline available, thresholds pending
- Geometry/operator compatibility rejections
  - Source: `tests/test_simulation_architecture.py`
  - Compared in: future domain-extension tests
  - Status: baseline available

## Prior Artifacts and Baselines

- `paper_runs/fusion_transport_paper_001/`: historical overnight-paper artifacts; preserve as prior work but not as the active program contract
- `run_config.yaml`: historical overnight run configuration; not the current program authority
- `README.md`: user-facing summary of the simulation-first repo positioning

## Open Reference Questions

- Which plasma / MHD benchmark or literature anchor should become the decisive external reference for Phase 3?
- Which benchmark suite should anchor long-horizon rollout claims in Phase 2?
- Which venue-specific prior art should anchor the first paper candidate?

## Background Reading

- Brandstetter-style geometric deep learning as the theoretical bridge for geometry/symmetry/operator design
- neuraloperator for structured operator learning on regular grids
- GraphCast design patterns for graph/mesh autoregressive forecasting
- SciML literature on structure-preserving integration and rollout diagnostics
- e3nn references for Euclidean-equivariant states and operators

---

_Reference map: 2026-03-18_
