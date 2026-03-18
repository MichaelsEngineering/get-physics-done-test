# Project Map

**Analysis Date:** 2026-03-18

## Program Definition

**Project:** `sentinel-multiscale-field-dynamics`

**Mission:** Decompose multiscale field dynamics into falsifiable subproblems that can be executed in stages and turned into paper-ready claims.

**Program Spine:** `geometry -> symmetry -> operator class -> closure -> integrator`

## Domain Map

| Domain | Central Question | Current Repo Anchor | Next Falsifiable Step |
| ------ | ---------------- | ------------------- | --------------------- |
| Fluid turbulence | Can the grid baseline preserve stability and invariants over long horizons? | `src/sentinel_core/problems/turbulence.py` | Add horizon and drift thresholds |
| Plasma / MHD | What extra state, symmetry, and constraints are required beyond the fluid case? | `src/sentinel_core/geometry/`, `src/sentinel_core/operators/` | Define minimal benchmark with domain constraints |
| Cross-scale surrogate modeling | Does a learned closure transfer across resolution and forcing scales? | `src/sentinel_core/core.py` | Create explicit train/test scale splits |
| Invariant-preserving learned dynamics | Which invariants must be enforced versus monitored? | `src/sentinel_core/integrators/sciml.py` | Add invariant-specific checks and projections |
| Long-horizon rollout stability | Which failure appears first: drift, blow-up, bias, or phase error? | `src/sentinel_core/core.py` rollout diagnostics | Add horizon sweep benchmarks |
| Closure modeling for unresolved scales | Which closure target is most stable under rollout? | `src/sentinel_core/closure/` | Compare residual forms and ablations |

## Falsifiable Subproblems

### SP-01 Grid turbulence stability

- Hypothesis: a closure-plus-integrator design can keep toy turbulence rollouts bounded while controlling drift.
- Observable: `energy_drift`, `enstrophy_drift`, bounded state norms.
- Falsifier: drift or instability grows beyond milestone thresholds over target horizons.
- Current files: `src/sentinel_core/core.py`, `src/sentinel_core/problems/turbulence.py`, `tests/test_simulation_architecture.py`

### SP-02 Constraint-preserving extension to plasma / MHD

- Hypothesis: the theory chain remains valid when additional constraints such as divergence conditions are introduced.
- Observable: task definitions retain a shared interface while representing plasma-specific constraints.
- Falsifier: plasma tasks require bypassing the geometry/symmetry/operator/closure/integrator chain.
- Current files: `src/sentinel_core/geometry/`, `src/sentinel_core/operators/`, `src/sentinel_core/integrators/`

### SP-03 Cross-scale transfer

- Hypothesis: closures trained on one resolution or forcing band transfer meaningfully to another.
- Observable: maintained stability and bounded invariant drift under scale-shifted evaluation.
- Falsifier: good in-distribution one-step scores but rapid degradation under scale transfer.
- Current files: `src/sentinel_core/core.py`, future evaluation scripts

### SP-04 Regime-shift robustness

- Hypothesis: invariant-aware rollout improves robustness under changed forcing, viscosity, or magnetic parameters.
- Observable: smaller degradation in stability and diagnostics under shift.
- Falsifier: invariant-aware variants fail as badly as unconstrained ones when the regime changes.
- Current files: `src/sentinel_core/config.py`, `src/sentinel_core/integrators/sciml.py`

## Failure Mode Registry

| Failure Mode | Why It Matters | First Detection Surface | Escalation Path |
| ------------ | -------------- | ----------------------- | --------------- |
| Energy drift | Indicates nonphysical rollout behavior | `run_rollout()` diagnostics in `src/sentinel_core/core.py` | Tighten integrator or closure target |
| Instability in long rollouts | Invalidates long-horizon surrogate use | Phase-2 horizon benchmarks | Add stability gates and ablations |
| Failure across scale transfer | Breaks unification claim | Phase-4 evaluation splits | Revisit state/operator choice |
| Violation of conservation constraints | Breaks physics-first contract | Integrator and validation docs | Add hard constraints or projections |
| Weakness under regime shift | Indicates brittle learned dynamics | Phase-4 robustness benchmarks | Expand training protocol or model class |

## Milestone Dependency Graph

1. Research Mapping -> define program objects and falsification gates
2. Grid Turbulence Core -> establish executable baseline evidence
3. Plasma / MHD Extension -> test shared architecture under stronger constraints
4. Cross-Scale + Regime Robustness -> test generalization claims
5. Paper Packaging -> write only from completed evidence-bearing milestones

---

_Project map: 2026-03-18_
