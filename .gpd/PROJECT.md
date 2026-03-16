# Fusion Transport Paper Overnight Draft

## What This Is

This project uses GPD inside Codex to produce a bounded overnight draft paper on reduced-order predictive models for turbulence-driven confinement degradation in tokamaks. The immediate deliverable is a traced, evidence-backed manuscript package that can be reviewed and revised after the unattended run.

## Core Research Question

Can a reduced-order turbulence-to-confinement model be framed as a credible control and commercialization wedge for tokamak operations, with enough evidence and caveats to support a draft paper?

## Scoping Contract Summary

### Contract Coverage

- Draft paper package: produce a complete markdown and LaTeX manuscript under `paper_runs/fusion_transport_paper_001/09_final/`
- Evidence-backed positioning: tie the thesis to literature summaries, extracted claims, and explicit disagreement mapping
- False progress to reject: polished prose or figures without source traceability and a written limitations section

### User Guidance To Preserve

- **User-stated observables:** turbulence-driven confinement degradation, reduced-order predictive control framing, commercialization relevance
- **User-stated deliverables:** finished paper at the end of a 5-hour run, intermediate artifacts on disk, tracked agent work
- **Must-have references / prior outputs:** literature review outputs created during the run and the run artifact tree under `paper_runs/fusion_transport_paper_001/`
- **Stop / rethink conditions:** if the decisive literature base is too thin, if claim extraction does not support the thesis, or if the final package cannot be assembled before the hard stop

### Scope Boundaries

**In scope**

- Literature-backed drafting workflow for a bounded overnight paper run
- Reduced-order model framing, field disagreements, commercialization wedge, and risks/limitations
- Agent traceability and run artifact organization

**Out of scope**

- New numerical plasma simulations
- Experimental validation beyond literature comparison
- Claims of deployable control performance not supported by written evidence

### Active Anchor Registry

- `Ref-run-plan`: `PLAN.md` and `run_config.yaml`
  - Why it matters: defines the required output contract and runtime limits
  - Carry forward: planning, execution, verification, writing
  - Required action: read, use, compare
- `Ref-output-tree`: `paper_runs/fusion_transport_paper_001/`
  - Why it matters: stable destination for all generated artifacts and trace outputs
  - Carry forward: execution, verification, writing
  - Required action: use

### Carry-Forward Inputs

- `PLAN.md`
- `run_config.yaml`
- `paper_runs/fusion_transport_paper_001/trace.json`

### Skeptical Review

- **Weakest anchor:** benchmark literature set is not yet selected and must be established during the run
- **Unvalidated assumptions:** reduced-order framing can support both technical and commercialization claims in one draft
- **Competing explanation:** the topic may only support a scoped review note rather than a full argument-driven paper
- **Disconfirming observation:** extracted literature claims do not support a coherent thesis with explicit limitations
- **False progress to reject:** section files created without citations, evidence map, or disagreement analysis

### Open Contract Questions

- Which specific papers will serve as decisive benchmark anchors for the overnight draft?
- Does the overnight run produce an argument-driven paper or only a structured literature synthesis?

## Research Questions

### Answered

(None yet)

### Active

- [ ] Which literature anchors best support the confinement degradation thesis?
- [ ] What reduced-order modeling frame is specific enough to defend without overclaiming?
- [ ] Which commercialization claims are supportable from the literature versus speculative?

### Out of Scope

- Closed-loop controller implementation and validation — requires simulation or experiment not planned for this run

## Research Context

### Physical System

Magnetically confined fusion plasmas in tokamaks, with emphasis on turbulence-driven transport and confinement degradation.

### Theoretical Framework

Reduced-order transport and control-oriented modeling grounded in plasma transport literature.

### Key Parameters and Scales

| Parameter | Symbol | Regime | Notes |
| --------- | ------ | ------ | ----- |
| Energy confinement time | `tau_E` | Device- and regime-dependent | Primary confinement metric |
| Heat transport level | `chi_eff` | Reduced-order / inferred | Used qualitatively unless benchmarked |
| Control latency budget | `tau_ctrl` | Operational constraint | Relevant to control framing, not yet quantified |

### Known Results

- Turbulent transport strongly constrains tokamak confinement performance
- Reduced-order models are commonly used where full-fidelity simulation is too expensive for control workflows

### What Is New

This project focuses on turning that body of work into a bounded, evidence-traceable paper draft with explicit disagreement and commercialization framing.

### Target Venue

Initial output is a draft manuscript package rather than a committed journal target.

### Computational Environment

Local Codex + GPD environment with filesystem-backed artifact output and runtime tracing.

## Notation and Conventions

See `.gpd/CONVENTIONS.md` for project conventions.

## Unit System

SI units unless a cited source requires another convention.

## Requirements

See `.gpd/REQUIREMENTS.md`.

## Key References

- `Ref-run-plan` — execution contract for the overnight run
- Benchmark literature set TBD during Phase 1

## Constraints

- **Time**: Hard stop at 04:00 America/New_York — final assembly must finish within the 5-hour window
- **Evidence**: The draft must remain tied to cited literature artifacts written during the run
- **Workflow**: All intermediate artifacts and trace summaries must be written under `paper_runs/fusion_transport_paper_001/`

## Key Decisions

| Decision | Rationale | Outcome |
| -------- | --------- | ------- |
| Use a single overnight run directory | Keeps outputs and traceability stable | Adopted |
| Require an explicit trace artifact | User asked for agent work tracking | Adopted |

---

_Last updated: 2026-03-15 after overnight run unblocker setup_
