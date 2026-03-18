# Requirements: Sentinel Multiscale Field Dynamics

**Defined:** 2026-03-18
**Core Research Question:** Can multiscale field dynamics across fluid turbulence and plasma / MHD be organized into a unified, invariant-aware learning-and-rollout program that remains stable over long horizons, transfers across scales and regimes, and yields paper-ready falsifiable claims at each stage?

## Primary Requirements

### Mapping and Planning

- [ ] **MAP-01**: Produce a project map that decomposes the program into falsifiable subproblems with explicit anchors to code and documentation
- [ ] **MAP-02**: Produce roadmap and milestone structure that connects turbulence, plasma / MHD, closure modeling, and verification work
- [ ] **MAP-03**: Produce paper outline candidates tied to executable evidence paths

### Simulation Core

- [ ] **SIM-01**: Maintain a working regular-grid turbulence baseline under `src/sentinel_core/`
- [ ] **SIM-02**: Make failure-mode diagnostics explicit for energy drift, rollout instability, and mean / invariant preservation
- [ ] **SIM-03**: Add milestone-ready extension points for plasma / MHD state variables, closures, and integrators without breaking the theory chain

### Generalization and Robustness

- [ ] **GEN-01**: Define scale-transfer tests that distinguish interpolation from genuine cross-scale generalization
- [ ] **GEN-02**: Define regime-shift tests that expose brittle learned dynamics
- [ ] **GEN-03**: Define conservation and constraint checks appropriate to each target domain

### Validation

- [ ] **VALD-01**: Require every milestone to specify quantitative pass / fail criteria
- [ ] **VALD-02**: Require long-horizon rollout evaluation beyond one-step prediction quality
- [ ] **VALD-03**: Require conservation/invariant tracking in both training and evaluation-facing artifacts
- [ ] **VALD-04**: Maintain tests and verification docs that map directly onto the current executable baseline

## Follow-up Requirements

### Plasma / MHD Expansion

- **PLSM-01**: Add a minimal plasma / MHD benchmark problem with clearly stated conserved quantities and constraints
- **PLSM-02**: Compare learned closures across fluid and plasma settings to identify what transfers and what fails

### Research Output

- **PAPR-01**: Produce at least one paper-ready result around the grid turbulence baseline with executable evidence
- **PAPR-02**: Produce a program paper or perspective piece on the unification framework once at least two domains share the same verification scaffold

## Out of Scope

| Topic | Reason |
| ----- | ------ |
| Production control claims | Requires validated surrogate-control loops beyond current repo scope |
| Full reactor design or experiment interpretation | Not supported by current codebase or data |
| Benchmark-chasing without invariant-aware diagnostics | Violates the project’s physics-first contract |

## Accuracy and Validation Criteria

| Requirement | Accuracy Target | Validation Method |
| ----------- | --------------- | ----------------- |
| SIM-01 | Grid turbulence task builds and rolls out deterministically | `pytest` plus CLI smoke runs |
| SIM-02 | Drift metrics are emitted and remain bounded on toy rollouts | Inspect rollout diagnostics and regression tests |
| GEN-01 | Cross-scale tests specify train/test resolution split and failure criteria | Research-map validation and milestone specs |
| VALD-02 | Every milestone includes horizon-based stability checks | Roadmap phase gate review |
| VALD-03 | Conserved quantities are listed, monitored, and interpreted | Validation docs and test extensions |

## Contract Coverage

| Requirement | Decisive Output / Deliverable | Anchor / Benchmark / Reference | Prior Inputs / Baselines | False Progress To Reject |
| ----------- | ----------------------------- | ------------------------------ | ------------------------ | ------------------------ |
| MAP-01 | `.gpd/research-map/PROJECT_MAP.md` | `PLAN.md`, `docs/architecture.md`, `src/sentinel_core/` | Existing theory-chain package | Narrative mapping without executable anchors |
| SIM-01 | Working grid turbulence baseline | `src/sentinel_core/problems/turbulence.py` | Current tests and CLI smoke path | New abstractions without runnable rollout |
| GEN-02 | Regime-shift evaluation design | Future milestone artifacts plus `.gpd/research-map/VALIDATION.md` | Existing grid baseline | Accuracy-only evaluation |
| PAPR-01 | Paper outline candidate with evidence path | `.gpd/research-map/PAPER_OUTLINES.md` | Research map and validation strategy | Venue positioning without milestone evidence |

## Traceability

| Requirement | Phase | Status |
| ----------- | ----- | ------ |
| MAP-01 | Phase 1: Research Mapping | In Progress |
| MAP-02 | Phase 1: Research Mapping | In Progress |
| MAP-03 | Phase 1: Research Mapping | In Progress |
| SIM-01 | Phase 2: Grid Turbulence Core | Planned |
| SIM-02 | Phase 2: Grid Turbulence Core | Planned |
| SIM-03 | Phase 3: Plasma / MHD Extension | Planned |
| GEN-01 | Phase 4: Cross-Scale Transfer | Planned |
| GEN-02 | Phase 4: Cross-Scale Transfer | Planned |
| GEN-03 | Phase 3: Plasma / MHD Extension | Planned |
| VALD-01 | All Phases | Planned |
| VALD-02 | All Phases | Planned |
| VALD-03 | All Phases | Planned |
| VALD-04 | All Phases | Planned |

---

_Requirements defined: 2026-03-18_
_Last updated: 2026-03-18 after research-program remap_
