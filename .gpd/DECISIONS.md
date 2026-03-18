# Decisions

## 2026-03-15

- Created a minimal GPD project scaffold so the overnight paper run could be planned and executed with stateful tracking.
- Standardized all required outputs under `paper_runs/fusion_transport_paper_001/`.
- Added a dedicated trace summary artifact to capture agent-stage ownership and execution status.

## 2026-03-18

- Reframed the repository from an overnight paper contract into a staged physics-first research program on multiscale turbulence and plasma dynamics.
- Adopted `geometry -> symmetry -> operator class -> closure -> integrator` as the program-wide organizing theory chain.
- Chosen the regular-grid turbulence path in `src/sentinel_core/` as the first executable falsification baseline.
- Kept graph and equivariant paths as contract-relevant scaffolds rather than overstating them as finished implementations.
- Made failure modes first-class project objects: energy drift, long-rollout instability, scale-transfer failure, conservation-law violation, and regime-shift weakness.
