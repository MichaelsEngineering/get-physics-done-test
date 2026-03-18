# Research State

## Project Reference

See: `.gpd/PROJECT.md` (updated 2026-03-18)

**Machine-readable scoping contract:** `.gpd/state.json` field `project_contract`

**Core research question:** Can multiscale field dynamics across fluid turbulence and plasma / MHD be organized into a unified, invariant-aware learning-and-rollout program that remains stable over long horizons, transfers across scales and regimes, and yields paper-ready falsifiable claims at each stage?
**Current focus:** Phase 1: Research Mapping

## Current Position

**Current Phase:** 01
**Current Phase Name:** Research Mapping
**Total Phases:** 5
**Current Plan:** 1
**Total Plans in Phase:** 3
**Status:** In Progress
**Last Activity:** 2026-03-18
**Last Activity Description:** Remapped the project as a multiscale turbulence and plasma research program

**Progress:** [█░░░░░░░░░] 10%

## Active Calculations

- No heavy numerical campaigns are active yet; the current work product is the research map and milestone decomposition.

## Intermediate Results

- The repository contains a working grid turbulence baseline under `src/sentinel_core/`
- Basic invariance/stability diagnostics are already emitted in the rollout result
- Graph and equivariant scaffolds exist on the same task-building interface

## Open Questions

- Which invariants should be hard constraints versus monitored diagnostics in each target domain?
- What minimal plasma / MHD task is strong enough to test the unification claim without overextending the current codebase?
- Which paper arc should be prioritized after the grid turbulence milestone is hardened?

## Performance Metrics

| Label | Duration | Tasks | Files |
| ----- | -------- | ----- | ----- |
| research-map | 00:00 | 0 | 0 |

## Accumulated Context

### Decisions

Full log: `.gpd/DECISIONS.md`

**Recent high-impact:**

- [Phase 1]: Adopt the theory chain as the project spine
- [Phase 1]: Keep grid turbulence as the first executable baseline
- [Phase 1]: Track energy drift, long-rollout instability, scale-transfer failure, conservation-law violation, and regime-shift weakness as named failure modes

### Active Approximations

| Approximation | Validity Range | Controlling Parameter | Current Value | Status |
| ------------- | -------------- | --------------------- | ------------- | ------ |
| Toy turbulence baseline is an adequate first falsification surface | Phase 2 grid-only work | Task complexity and invariants covered | Limited | Active |
| Graph/equivariant scaffolds can remain non-production while still informing roadmap design | Phase 1 mapping through Phase 3 planning | API stability | Moderate | Active |

**Convention Lock:**

- Unit system: dimensionless simulation units unless task-specific physics requires SI or normalized plasma units
- Architecture lock: all new dynamics must resolve through geometry, symmetry, operator class, closure, and integrator

### Propagated Uncertainties

| Quantity | Current Value | Uncertainty | Last Updated (Phase) | Method |
| -------- | ------------- | ----------- | -------------------- | ------ |
| Domain-transfer viability | TBD | High | Phase 1 | Research mapping and milestone definition |
| Long-horizon stability ceiling | TBD | High | Phase 1 | To be measured in Phase 2 |

### Pending Todos

- Materialize `.gpd/research-map/` as the authority for formalism, references, architecture, structure, conventions, validation, and concerns
- Select the first paper arc after Phase 2 evidence exists

### Blockers/Concerns

- Plasma / MHD extension is not implemented yet
- Verification criteria for scale transfer and regime shift are not yet executable

## Session Continuity

**Last session:** 2026-03-18
**Stopped at:** Research map creation and milestone decomposition
**Resume file:** `PLAN.md`
