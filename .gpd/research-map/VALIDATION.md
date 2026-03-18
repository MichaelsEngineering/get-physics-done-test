# Validation and Cross-Checks

**Analysis Date:** 2026-03-18

## Failure-Mode Coverage

| Failure Mode | Current Check Surface | Current Status | Next Required Check |
| ------------ | --------------------- | -------------- | ------------------- |
| Energy drift | `run_rollout()` diagnostics in `src/sentinel_core/core.py` | Partially covered | Add thresholded regression tests over longer horizons |
| Instability in long rollouts | Short smoke rollout only | Weakly covered | Add horizon sweep and boundedness tests |
| Failure across scale transfer | Not implemented | Missing | Add resolution-transfer protocol |
| Violation of conservation constraints | Mean projection plus drift reporting | Partially covered | Add invariant-specific assertions and future plasma constraints |
| Weakness under regime shift | Not implemented | Missing | Add forcing/parameter shift benchmarks |

## Analytic Cross-Checks

**Current checks:**

- Invalid geometry/operator combinations are rejected
  - File: `tests/test_simulation_architecture.py`
- Integrator rejects unstable or invalid `dt`
  - File: `src/sentinel_core/integrators/sciml.py`

**Missing checks:**

- Limiting behavior for vanishing closure contribution
- Sensitivity to timestep and viscosity changes
- Plasma / MHD-specific constraint checks once that benchmark exists

## Numerical Validation

**Existing Tests:**

- `tests/test_simulation_architecture.py`: theory-chain compatibility, grid rollout sanity, graph/equivariant scaffolds, training stub
- `tests/test_cli.py`: architecture and smoke-run CLI surface
- `tests/test_check_env.py`, `tests/test_security_tools.py`: workflow support tooling

**Run Commands:**

```bash
.venv/bin/pytest -q
.venv/bin/python -m src.gpd_test.cli smoke-grid --steps 2
```

## Required New Validation Phases

### Phase 2

- Add long-horizon drift and boundedness thresholds
- Add ablation tests for projection on/off and closure variants
- Record acceptable drift envelopes for toy turbulence

### Phase 3

- Add plasma / MHD constraint checks such as divergence-related conditions
- Verify shared task contract still covers both domains

### Phase 4

- Add scale-transfer splits across resolution or forcing scales
- Add regime-shift splits across viscosity, forcing, or domain parameters
- Reject models that only improve one-step metrics without long-horizon robustness

## Missing Tests

- Explicit long-horizon stability regression
- Cross-scale generalization benchmark
- Regime-shift benchmark
- Domain-specific conservation checks for plasma / MHD

## Reproducibility

**Random Seeds:**

- Current turbulence seeds are deterministic functions, not stochastic draws
  - File: `src/sentinel_core/geometry/grid.py`

**Version Pinning:**

- Core dependency declarations live in `pyproject.toml`
- Optional extras exist for `sim`, `graph`, and `equivariant`

---

_Validation analysis: 2026-03-18_
