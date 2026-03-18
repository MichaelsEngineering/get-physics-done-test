# Conventions Ledger

**Project:** Sentinel Multiscale Field Dynamics
**Created:** 2026-03-18
**Last updated:** 2026-03-18 (Phase 1)

> This file is append-only for convention entries. When a convention changes, add a new
> entry with the updated value and mark the old entry as superseded.

---

## Units

### Unit System

| Field | Value |
| ----- | ----- |
| **Convention** | Use dimensionless simulation units for toy turbulence and learning-system diagnostics unless a milestone explicitly requires SI or normalized plasma units |
| **Introduced** | Phase 1 |
| **Rationale** | Keeps early-stage verification focused on invariants, transfer, and rollout behavior rather than unit-conversion ambiguity |
| **Dependencies** | Rollout diagnostics, future benchmark definitions, validation reports |

## Program Architecture

### Theory Chain

| Field | Value |
| ----- | ----- |
| **Convention** | All executable research tasks must resolve through `geometry -> symmetry -> operator class -> closure -> integrator` |
| **Introduced** | Phase 1 |
| **Rationale** | Prevents architecture drift and keeps physical assumptions visible |
| **Dependencies** | `src/sentinel_core/`, roadmap milestones, paper framing |

## Dynamics Framing

### Learned Components

| Field | Value |
| ----- | ----- |
| **Convention** | Learned modules are closures or residual corrections attached to resolved dynamics, not unconstrained replacements for the full physical system |
| **Introduced** | Phase 1 |
| **Rationale** | Keeps the project aligned with invariant-aware and structure-preserving rollout goals |
| **Dependencies** | Closure design, verification strategy, paper claims |

## Verification Language

### Failure Modes

| Field | Value |
| ----- | ----- |
| **Convention** | Track energy drift, long-rollout instability, cross-scale transfer failure, conservation-law violation, and regime-shift weakness as first-class failure modes |
| **Introduced** | Phase 1 |
| **Rationale** | Forces research outputs to stay falsifiable and physically grounded |
| **Dependencies** | Requirements, roadmap, validation docs, paper outlines |
