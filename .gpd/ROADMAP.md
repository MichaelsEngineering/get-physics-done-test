# Roadmap: Sentinel Multiscale Field Dynamics

## Overview

This roadmap turns the repository into a staged physics-first research program. The near-term path is: establish the research map, harden the grid turbulence baseline, extend the state/invariant language to plasma / MHD, then test cross-scale transfer and regime robustness before packaging paper-ready claims.

## Contract Overview

| Contract Item | Advanced By Phase(s) | Status |
| ------------- | -------------------- | ------ |
| Physics-first project map | Phase 1 | In Progress |
| Executable grid turbulence baseline | Phase 2 | Planned |
| Plasma / MHD extension scaffold | Phase 3 | Planned |
| Cross-scale and regime-shift verification | Phase 4 | Planned |
| Paper-ready evidence paths | Phases 2-5 | Planned |

## Milestones

- [ ] **Milestone 1: Research Map and Baseline Contract**
- [ ] **Milestone 2: Grid Turbulence Verification Core**
- [ ] **Milestone 3: Plasma / MHD State Extension**
- [ ] **Milestone 4: Cross-Scale Generalization and Regime Shift**
- [ ] **Milestone 5: Paper Production**

## Phases

- [ ] **Phase 1: Research Mapping**
- [ ] **Phase 2: Grid Turbulence Core**
- [ ] **Phase 3: Plasma / MHD Extension**
- [ ] **Phase 4: Cross-Scale Transfer and Regime Robustness**
- [ ] **Phase 5: Paper Packaging**

## Phase Details

### Phase 1: Research Mapping

**Goal:** Produce the project map, requirements, roadmap, open questions, verification strategy, and paper outline candidates
**Depends on:** Current repo structure and simulation baseline
**Requirements:** [MAP-01, MAP-02, MAP-03]
**Success Criteria:**

1. `.gpd/research-map/` contains the authoritative map documents
2. `PROJECT.md`, `REQUIREMENTS.md`, and `ROADMAP.md` align with the new program
3. Failure modes and verification gates are explicit

**Plans:** 3 plans

- [ ] 01-01: Map theory, computation, conventions, and status
- [ ] 01-02: Define requirements, milestones, and verification strategy
- [ ] 01-03: Draft paper outline candidates and milestone evidence paths

### Phase 2: Grid Turbulence Core

**Goal:** Turn the regular-grid turbulence path into a credible falsification and verification baseline
**Depends on:** Phase 1
**Requirements:** [SIM-01, SIM-02, VALD-01, VALD-02, VALD-03, VALD-04]
**Success Criteria:**

1. The grid turbulence task remains executable from CLI and tests
2. Conservation and drift diagnostics are emitted and regression-tested
3. Long-horizon stability checks exist beyond one-step rollout quality

**Plans:** 4 plans

- [ ] 02-01: Strengthen turbulence diagnostics and invariant accounting
- [ ] 02-02: Add horizon-based rollout benchmarks and regression thresholds
- [ ] 02-03: Add failure-case tests for instability and conservation violations
- [ ] 02-04: Package a first paper-ready vertical slice

### Phase 3: Plasma / MHD Extension

**Goal:** Extend the theory chain to a minimal plasma / MHD problem without collapsing into a separate architecture
**Depends on:** Phase 2
**Requirements:** [SIM-03, GEN-03, PLSM-01, PLSM-02, VALD-01, VALD-03]
**Success Criteria:**

1. A minimal plasma / MHD benchmark is defined with explicit geometry, symmetry, operator, closure, and integrator choices
2. Domain constraints such as divergence or flux-related invariants are represented in verification design
3. Shared abstractions still cover both turbulence and plasma tasks

**Plans:** 4 plans

- [ ] 03-01: Define minimal plasma / MHD benchmark and state variables
- [ ] 03-02: Add domain-specific constraints and invariants
- [ ] 03-03: Compare closure targets across fluid and plasma settings
- [ ] 03-04: Write extension-specific validation notes

### Phase 4: Cross-Scale Transfer and Regime Robustness

**Goal:** Test whether the learned dynamics generalize beyond the narrow training regime
**Depends on:** Phases 2-3
**Requirements:** [GEN-01, GEN-02, GEN-03, VALD-01, VALD-02, VALD-03]
**Success Criteria:**

1. Resolution-transfer and forcing/regime-shift splits are defined and executable
2. Failure modes are observable through explicit diagnostics
3. Generalization claims are rejected when only short-horizon metrics improve

**Plans:** 4 plans

- [ ] 04-01: Define cross-scale split protocol
- [ ] 04-02: Define regime-shift benchmarks
- [ ] 04-03: Add ablations for invariant enforcement and closure choice
- [ ] 04-04: Summarize robustness findings for paper use

### Phase 5: Paper Packaging

**Goal:** Produce paper-ready outputs grounded in completed milestone evidence
**Depends on:** At least one completed evidence-bearing milestone
**Requirements:** [PAPR-01, PAPR-02]
**Success Criteria:**

1. At least one outline candidate is fully supported by completed artifacts
2. Claims are traceable to verification results, not only architecture rationale
3. The chosen paper arc is matched to the strongest available milestone evidence

**Plans:** 3 plans

- [ ] 05-01: Select paper arc and evidence package
- [ ] 05-02: Draft manuscript structure and figures
- [ ] 05-03: Run review and revise with milestone traceability

## Progress

**Execution Order:** Phases execute in numeric order, but Phase 5 can begin only after Phase 2 or later yields paper-grade evidence.

| Phase | Plans Complete | Status | Completed |
| ----- | -------------- | ------ | --------- |
| 1. Research Mapping | 0/3 | In Progress | - |
| 2. Grid Turbulence Core | 0/4 | Ready after Phase 1 | - |
| 3. Plasma / MHD Extension | 0/4 | Blocked on Phase 2 | - |
| 4. Cross-Scale Transfer and Regime Robustness | 0/4 | Blocked on Phases 2-3 | - |
| 5. Paper Packaging | 0/3 | Blocked on milestone evidence | - |
