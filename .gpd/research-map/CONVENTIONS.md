# Conventions and Methodology

**Analysis Date:** 2026-03-18

## Program Conventions

**Theory-chain lock:**

- Every executable task must resolve through geometry, symmetry, operator class, closure, and integrator
- Files: `src/sentinel_core/core.py`, `.gpd/CONVENTIONS.md`

**Learned dynamics framing:**

- Learned modules are closures or residuals attached to resolved dynamics
- Files: `src/sentinel_core/closure/`, `docs/architecture.md`

**Units:**

- Use dimensionless simulation units for the current turbulence baseline unless a domain-specific task states otherwise
- Files: `.gpd/CONVENTIONS.md`, `.gpd/PROJECT.md`

## Assumptions Catalog

**Explicit Assumptions:**

- The toy turbulence baseline is an acceptable first falsification surface
  - Files: `src/sentinel_core/problems/turbulence.py`, `.gpd/ROADMAP.md`
- Graph and equivariant paths are scaffolds, not fully validated solvers
  - Files: `docs/architecture.md`, `.gpd/PROJECT.md`

**Implicit Assumptions:**

- The same decomposition logic will remain useful for plasma / MHD tasks
  - Files: `src/sentinel_core/core.py`, `.gpd/ROADMAP.md`
  - Risk: plasma constraints may require richer state and integrator logic

## Sign and Factor Conventions

**Current state:**

- No advanced field-theory sign conventions are yet encoded in the simulation package
- The important convention is architectural rather than algebraic: constraints and invariants are first-class objects, not post hoc metrics

## Notation Consistency

**Consistent Usage:**

- `geometry`, `symmetry`, `operator`, `closure`, `integrator` keep stable meanings across docs and code
- `energy_drift`, `enstrophy_drift`, and `mean_value` are current rollout diagnostics

**Potential Conflicts to Watch:**

- Future plasma / MHD work must avoid overloading fluid-only quantities as if they were universal invariants
- Future graph/equivariant work must distinguish representation metadata from physical observables

---

_Methodology analysis: 2026-03-18_
