# Research Gaps and Open Issues

**Analysis Date:** 2026-03-18

## Numerical Concerns

**Long-horizon stability is under-tested:**

- Problem: current smoke rollouts are too short to support stability claims
- Files: `src/sentinel_core/core.py`, `tests/test_simulation_architecture.py`
- Symptoms: stable short runs but delayed blow-up or drift
- Resolution: add horizon sweeps and thresholded regression tests

**Cross-scale transfer is unmapped in code:**

- Problem: no executable resolution-transfer protocol exists
- Files: `src/sentinel_core/core.py`, `.gpd/ROADMAP.md`
- Symptoms: claims of generalization remain speculative
- Resolution: add explicit train/test scale splits

## Physical Consistency Issues

**Conservation set is too narrow:**

- Concern: the current baseline tracks energy, enstrophy, and mean, but not the full invariant set that future plasma tasks will need
- Files: `src/sentinel_core/core.py`, `src/sentinel_core/integrators/sciml.py`
- Impact: weakens any broad unification claim
- Resolution path: define domain-specific invariant registries by milestone

## Missing Generalizations

**Minimal plasma / MHD benchmark is absent:**

- Current scope: grid turbulence vertical slice only
- Natural extension: add a constrained plasma / MHD task with explicit state and invariants
- Difficulty: moderate to hard
- Blocks: milestone-3 execution and any true cross-domain paper claim

## Missing Literature Connections

**Paper anchors are not yet grounded in the repo:**

- What: the repo names design inspirations but does not yet attach a benchmark paper stack to each milestone
- Why relevant: paper production requires stronger external comparison anchors
- Priority: high

## Placeholder and Stub Content

**Graph and equivariant paths are scaffolds:**

- What: forward-pass placeholders without benchmark-quality validation
- Files: `src/sentinel_core/operators/graph.py`, `src/sentinel_core/operators/equivariant.py`
- Needed for: later unification milestones

## Priority Ranking

**Critical (blocks correctness):**

1. Long-horizon stability lacks thresholded verification.
2. Conservation coverage is too narrow for broad physics claims.

**High (blocks completeness):**

1. No plasma / MHD benchmark exists yet.
2. No cross-scale or regime-shift benchmark exists yet.

**Medium (improves quality):**

1. Paper candidates need explicit external benchmark anchors.

**Low (nice to have):**

1. Broader graph/equivariant benchmark coverage before Phase 3.

---

_Gap analysis: 2026-03-18_
