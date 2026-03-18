# Sentinel Multiscale Field Dynamics

## What This Is

This project uses Get Physics Done (GPD) inside Codex to organize a physics-first research program for multiscale turbulence and plasma dynamics. The repository is no longer centered on a single overnight paper run. It is now the authority for a staged program that turns the unification problem for multiscale field dynamics into falsifiable computational and theoretical subproblems.

The computational spine already present in `src/sentinel_core/` is:

`geometry -> symmetry -> operator class -> closure -> integrator`

This spine is the common language for grid turbulence, graph-based surrogate dynamics, and Euclidean-equivariant state representations.

## Core Research Question

Can multiscale field dynamics across fluid turbulence and plasma / MHD be organized into a unified, invariant-aware learning-and-rollout program that remains stable over long horizons, transfers across scales and regimes, and yields paper-ready falsifiable claims at each stage?

## Scoping Contract Summary

### Contract Coverage

- Build a staged research map for multiscale turbulence and plasma dynamics
- Define falsifiable requirements, milestones, and verification gates for the simulation program
- Produce paper-outline candidates tied to executable verification paths
- Preserve the existing GPD project machinery and the simulation package under `src/sentinel_core/`

### User Guidance To Preserve

- **User-stated domains:** fluid turbulence, plasma / MHD, cross-scale surrogate modeling, invariant-preserving learned dynamics, long-horizon rollout stability, closure modeling for unresolved scales
- **User-stated failure modes:** energy drift, rollout instability, scale-transfer failure, conservation-law violation, regime-shift weakness
- **User-stated deliverables:** project map, requirements, roadmap, open questions, verification strategy, paper outline candidates
- **Must-have implementation anchor:** `src/sentinel_core/` and its theory chain

### Scope Boundaries

**In scope**

- Regular-grid turbulence as the first executable vertical slice
- Plasma / MHD program decomposition and milestone planning
- Verification design for conservation, stability, transfer, and regime shift
- Paper planning tied to code and validation outputs

**Out of scope for the current map**

- Claims of solved plasma transport or production-ready control
- Full-fidelity MHD solver implementation in this mapping pass
- Experimental validation not represented in the repository

### Active Anchor Registry

- `Ref-program-plan`: `PLAN.md`
  - Why it matters: top-level statement of project scope, domains, and failure modes
  - Carry forward: planning, execution, writing
  - Required action: read, use
- `Ref-simulation-core`: `src/sentinel_core/`
  - Why it matters: current executable substrate for the program spine
  - Carry forward: planning, execution, verification, writing
  - Required action: read, extend, compare
- `Ref-architecture-report`: `docs/architecture.md`
  - Why it matters: explicit articulation of the geometry-to-integrator theory chain
  - Carry forward: planning, verification, writing
  - Required action: read, cite, align
- `Ref-tests`: `tests/test_simulation_architecture.py`, `tests/test_cli.py`
  - Why it matters: current behavioral checks for the working core and CLI surface
  - Carry forward: execution, verification
  - Required action: run, extend

### Carry-Forward Inputs

- `PLAN.md`
- `docs/architecture.md`
- `src/sentinel_core/core.py`
- `src/sentinel_core/problems/turbulence.py`
- `tests/test_simulation_architecture.py`

### Skeptical Review

- **Weakest anchor:** the repository currently has only a toy grid-turbulence vertical slice and scaffold-level graph/equivariant support
- **Unvalidated assumptions:** the same theory chain will scale from fluid turbulence to plasma / MHD without additional state variables, constraints, or geometry changes
- **Competing explanation:** long-horizon stability may depend more on integrator and diagnostic design than on learned operator quality
- **Disconfirming observation:** cross-scale transfer or regime-shift tests fail even when short-rollout metrics look good
- **False progress to reject:** adding more architectures or papers without executable conservation/stability checks

### Open Contract Questions

- Which invariants are mandatory across all target domains versus domain-specific?
- What is the smallest plasma / MHD extension that meaningfully tests the unification claim?
- Which paper should be written first: turbulence vertical slice, invariant-preserving rollout, or plasma-transfer roadmap?

## Research Questions

### Active

- [ ] Which geometric state representations best preserve physically meaningful invariants across grid, graph, and equivariant formulations?
- [ ] Which conserved quantities should be enforced directly by the integrator versus only monitored diagnostically?
- [ ] What closure targets are most stable for long-horizon rollout: residual tendencies, filtered subgrid stress, latent correction, or hybrid forms?
- [ ] How far does the grid-turbulence vertical slice transfer to plasma / MHD before state and symmetry assumptions break?
- [ ] Which regime-shift tests are decisive enough to reject brittle surrogate models early?

### Out of Scope

- Closed-loop control claims without verified surrogate and rollout performance
- Full deployment or reactor-operations claims

## Research Context

### Physical System

Multiscale nonlinear field dynamics with immediate focus on turbulent fluids and magnetized plasmas / MHD.

### Theoretical Framework

Geometric deep learning informed by symmetry, operator-learning ideas for structured states, and SciML-style structure-preserving rollout.

### Key Parameters and Scales

| Parameter | Symbol | Regime | Notes |
| --------- | ------ | ------ | ----- |
| Reynolds number | `Re` | Turbulence baseline | Controls inertial-to-dissipative balance |
| Magnetic Reynolds number | `Rm` | Plasma / MHD extension | Controls induction versus diffusion |
| Resolution ratio | `k_max / k_forcing` | Cross-scale surrogate tests | Tracks represented versus unresolved scales |
| Rollout horizon | `T_rollout` | Stability metric | Must extend well beyond one-step accuracy |
| Invariant drift | `Delta I(T)` | Verification metric | Covers energy, mass, circulation, divergence, and other conserved quantities |

### Known Results

- The repository contains a working regular-grid turbulence rollout with explicit diagnostics for energy drift, enstrophy drift, and mean preservation
- The project already encodes graph and equivariant scaffolds under the same task-building interface
- The current tests assert geometry-to-operator compatibility and basic rollout sanity

### What Is New

This mapping turns the repository from a single-paper scaffold into a staged research program with milestone structure, verification gates, and paper candidates tied directly to executable artifacts.

### Target Venues

- Machine-learning-for-physics or SciML venue for the invariant-preserving rollout story
- Plasma / fusion modeling venue for the turbulence-to-MHD extension
- General scientific machine learning venue for the geometry-to-integrator unification framework

### Computational Environment

Local Python 3.11 project with `uv`, `.venv`, Typer CLI entrypoints, GPD project metadata under `.gpd/`, and the simulation package under `src/sentinel_core/`.

## Notation and Conventions

See `.gpd/CONVENTIONS.md` and `.gpd/research-map/CONVENTIONS.md`.

## Unit System

Dimensionless simulation units for toy turbulence unless a task explicitly calls for SI or normalized plasma units.

## Requirements

See `.gpd/REQUIREMENTS.md`.

## Key References

- `Ref-program-plan`
- `Ref-simulation-core`
- `Ref-architecture-report`
- `Ref-tests`

## Constraints

- Every milestone must produce falsifiable outputs, not just conceptual descriptions
- The grid turbulence core remains the first execution baseline
- Plasma / MHD expansion must preserve the project’s theory-chain organization
- Failure modes must be tracked explicitly in verification artifacts

## Key Decisions

| Decision | Rationale | Outcome |
| -------- | --------- | ------- |
| Use the theory chain as the project spine | Keeps geometry, symmetry, learned closure, and rollout logic coupled in a physics-first way | Adopted |
| Keep grid turbulence as milestone-1 execution target | Provides a tractable executable baseline | Adopted |
| Treat graph and equivariant paths as scaffolded but contract-relevant | Preserves the intended unification path without pretending they are production-ready | Adopted |

---

_Last updated: 2026-03-18 after research-program remap_
