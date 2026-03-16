# Requirements: Fusion Transport Paper Overnight Draft

**Defined:** 2026-03-15
**Core Research Question:** Can a reduced-order turbulence-to-confinement model be framed as a credible control and commercialization wedge for tokamak operations, with enough evidence and caveats to support a draft paper?

## Primary Requirements

### Analysis

- [ ] **ANLY-01**: Build a source index covering at least the minimum literature set from `run_config.yaml`
- [ ] **ANLY-02**: Extract at least 30 claims into a table with source traceability
- [ ] **ANLY-03**: Map field disagreements and select a thesis consistent with the evidence

### Writing

- [ ] **WRIT-01**: Produce a complete paper outline and all required section drafts under the run directory
- [ ] **WRIT-02**: Produce final markdown and LaTeX paper drafts plus abstract, title options, and executive summary

### Validation

- [ ] **VALD-01**: Ensure every major claim in the final draft traces back to the evidence map or disagreement map
- [ ] **VALD-02**: Ensure the final package includes an explicit risks/limitations section
- [ ] **VALD-03**: Ensure trace artifacts record which agent role handled each stage of work

## Follow-up Requirements

### Future Technical Validation

- **FUTR-01**: Compare the paper thesis against simulation or experimental benchmarks
- **FUTR-02**: Quantify controller performance claims with explicit models

## Out of Scope

| Topic | Reason |
| ----- | ------ |
| New turbulence simulations | Not feasible within the bounded overnight writing run |
| Operational deployment claims | Requires evidence outside the current repo and run contract |

## Accuracy and Validation Criteria

| Requirement | Accuracy Target | Validation Method |
| ----------- | --------------- | ----------------- |
| ANLY-01 | At least 18 sources and 30 extracted claims | Compare artifact counts against `run_config.yaml` |
| WRIT-02 | All required final files exist | Filesystem verification under `paper_runs/fusion_transport_paper_001/09_final/` |
| VALD-03 | Every execution stage has a trace entry | Inspect `paper_runs/fusion_transport_paper_001/trace.json` |

## Contract Coverage

| Requirement | Decisive Output / Deliverable | Anchor / Benchmark / Reference | Prior Inputs / Baselines | False Progress To Reject |
| ----------- | ----------------------------- | ------------------------------ | ------------------------ | ------------------------ |
| ANLY-01 | `01_sources/source_index.json` | Run plan plus selected literature anchors | `PLAN.md`, `run_config.yaml` | Uncited section drafting |
| ANLY-03 | `03_disagreements/thesis_selected.md` | Disagreement map and evidence map | Claims table | Thesis chosen before claim extraction |
| WRIT-02 | `09_final/final_paper.md`, `09_final/final_paper.tex` | Final outline, section drafts, revision notes | All upstream run artifacts | Final prose without evidence coverage |
| VALD-03 | `trace.json` | Agent trace summary | Runtime trace events | Missing actor/stage linkage |

## Traceability

| Requirement | Phase | Status |
| ----------- | ----- | ------ |
| ANLY-01 | Phase 1: Overnight Paper Run | Pending |
| ANLY-02 | Phase 1: Overnight Paper Run | Pending |
| ANLY-03 | Phase 1: Overnight Paper Run | Pending |
| WRIT-01 | Phase 1: Overnight Paper Run | Pending |
| WRIT-02 | Phase 1: Overnight Paper Run | Pending |
| VALD-01 | Phase 1: Overnight Paper Run | Pending |
| VALD-02 | Phase 1: Overnight Paper Run | Pending |
| VALD-03 | Phase 1: Overnight Paper Run | Pending |

---

_Requirements defined: 2026-03-15_
_Last updated: 2026-03-15 after overnight run unblocker setup_
