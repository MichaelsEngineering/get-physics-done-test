# Paper Outline Candidates

**Analysis Date:** 2026-03-18

## Candidate 1: Invariant-Preserving Rollout for Grid Turbulence

**Thesis:** The geometry-to-integrator theory chain yields a clearer and more falsifiable turbulence surrogate baseline than accuracy-only operator-learning workflows.

**Evidence required:**

- Phase-2 long-horizon rollout benchmarks
- Drift and stability ablations
- Comparison between invariant-aware and weaker baselines

**Section arc:**

1. Motivation: why one-step accuracy is insufficient
2. Theory chain: geometry, symmetry, operator, closure, integrator
3. Grid turbulence benchmark and diagnostics
4. Long-horizon results and failure-mode analysis
5. Implications for learned scientific simulators

## Candidate 2: A Unifying Program for Multiscale Field Dynamics

**Thesis:** A single physics-first decomposition can organize turbulence, plasma / MHD, and structured learned dynamics without collapsing domain-specific constraints.

**Evidence required:**

- Completed research map
- Phase-2 turbulence baseline
- Phase-3 minimal plasma / MHD extension
- Shared validation framework

**Section arc:**

1. Program motivation and failure modes
2. Geometry-to-integrator unification framework
3. Turbulence baseline
4. Plasma / MHD extension requirements
5. Cross-scale and regime robustness agenda

## Candidate 3: Closure Modeling Under Scale Transfer and Regime Shift

**Thesis:** Closure designs that look competitive in-distribution can fail under cross-scale transfer and regime shift unless invariants and rollout dynamics are built into evaluation.

**Evidence required:**

- Phase-4 transfer and robustness benchmarks
- Closure ablations
- Diagnostics showing drift, instability, or conservation failure

**Section arc:**

1. Why closure evaluation is often misleading
2. Transfer and regime-shift benchmark design
3. Closure family comparisons
4. Failure mode taxonomy
5. Recommendations for surrogate evaluation

## Recommended First Paper

Start with **Candidate 1**. It aligns with the only currently executable domain in the repo and requires the least speculative extension beyond the current baseline.

---

_Paper outline analysis: 2026-03-18_
