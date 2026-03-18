# Theoretical Frameworks

**Analysis Date:** 2026-03-18

## Physical System

**Subject:** Multiscale nonlinear field dynamics with immediate focus on turbulent fluids and magnetized plasmas / MHD.

**Scales:**

- Length: forcing scale, inertial-range scales, dissipation scale, and future plasma characteristic lengths
- Time: fast local dynamics versus long rollout horizons `T_rollout`
- Dimensionless parameters: `Re`, `Rm`, resolution ratio, invariant drift `Delta I(T)`

**Degrees of Freedom:**

- Grid fields: vorticity and velocity channels
  - File: `src/sentinel_core/problems/turbulence.py`
- Graph states: node features and message-passing states
  - File: `src/sentinel_core/geometry/graph.py`
- Equivariant states: scalar and vector features with irrep hints
  - File: `src/sentinel_core/geometry/equivariant.py`

## Theoretical Framework

**Primary Framework:**

- Physics-first geometric learning for field dynamics
- Formulation: structured state geometry with symmetry-constrained operator families and structure-preserving rollout
- Files: `docs/architecture.md`, `src/sentinel_core/core.py`

**Secondary/Supporting Frameworks:**

- SciML-style structure-preserving integration
  - File: `src/sentinel_core/integrators/sciml.py`
- neuraloperator-style regular-grid closure design
  - File: `src/sentinel_core/closure/grid.py`
- GraphCast-inspired autoregressive graph processing
  - File: `src/sentinel_core/operators/graph.py`
- e3nn-inspired Euclidean-equivariant representation
  - File: `src/sentinel_core/operators/equivariant.py`

## Fundamental Equations

**Governing Equations:**

| Equation | Type | Location | Status |
| -------- | ---- | -------- | ------ |
| Grid rollout update `u_{t+1} = u_t + dt * (resolved + closure)` | discrete EOM | `src/sentinel_core/integrators/sciml.py` | Implemented |
| Laplacian stencil | differential operator | `src/sentinel_core/operators/grid.py` | Implemented |
| Advection-like tendency surrogate | constitutive / resolved dynamics | `src/sentinel_core/operators/grid.py` | Implemented |
| Closure prediction from local history | learned residual | `src/sentinel_core/closure/grid.py` | Implemented |

## Symmetries and Conservation Laws

**Exact Symmetries:**

- Periodic translation for grid states
  - File: `src/sentinel_core/symmetry/resolver.py`
- Permutation/locality for graph states
  - File: `src/sentinel_core/symmetry/resolver.py`
- Euclidean translation/rotation equivariance for geometric states
  - File: `src/sentinel_core/symmetry/resolver.py`

**Conservation Targets:**

- Mean preservation through mean-free projection
  - File: `src/sentinel_core/integrators/sciml.py`
- Energy and enstrophy tracking as current diagnostic observables
  - File: `src/sentinel_core/core.py`
- Future plasma / MHD targets: divergence constraints, flux-related invariants, and cross-helicity-style quantities
  - File: `.gpd/ROADMAP.md`

## Parameters and Couplings

**Fundamental Parameters:**

- `dt`: integrator time step
  - Defined in: `src/sentinel_core/config.py`
- `viscosity`: resolved operator dissipation coefficient
  - Defined in: `src/sentinel_core/config.py`
- `history`, `latent_width`: closure configuration
  - Defined in: `src/sentinel_core/config.py`

## Phase Structure / Regimes

**Regimes Studied:**

- Toy periodic 2D turbulence baseline
  - Files: `src/sentinel_core/problems/turbulence.py`, `src/sentinel_core/core.py`

**Known Limiting Cases:**

- Invalid geometry/operator pairings are rejected explicitly
  - File: `src/sentinel_core/core.py`
- Nonpositive or oversized `dt` is rejected by the integrator
  - File: `src/sentinel_core/integrators/sciml.py`

## Units and Conventions

**Unit System:**

- Dimensionless simulation units for current executable work
- File: `.gpd/CONVENTIONS.md`

**Key Conventions:**

- Learned dynamics are closures, not replacements for the full resolved dynamics
- Every task resolves through geometry, symmetry, operator class, closure, and integrator

---

_Framework analysis: 2026-03-18_
