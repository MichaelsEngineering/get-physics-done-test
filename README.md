# get-physics-done-test

Public research log exploring the use of Get Physics Done (GPD) with Codex for predictive control of plasma turbulence and confinement in fusion reactors.

This repository documents experiments using GPD as a structured research workflow that converts physics questions into bounded paper drafts and reproducible research artifacts.

## Goal

Evaluate whether GPD can accelerate early-stage research exploration in fusion control problems by producing structured drafts, literature summaries, and model proposals.

The specific focus is predictive control of tokamak plasma turbulence and confinement.

## What is GPD

Get Physics Done (GPD) is a structured research workflow system that organizes AI-assisted scientific exploration into reproducible plans, artifacts, and paper drafts.

Instead of generating free-form text, GPD runs structured research steps and writes all intermediate outputs to disk.

## Referenced software

This repository uses the following external research software:

```bibtex
@software{physical_superintelligence_2026_gpd,
  author = {{Physical Superintelligence PBC}},
  title = {Get Physics Done (GPD)},
  version = {1.1.0},
  year = {2026},
  url = {https://github.com/psi-oss/get-physics-done},
  license = {Apache-2.0}
}
```

## Stack

- Python 3.11
- uv (environment and dependency manager)
- Codex (reasoning and code generation)
- Get Physics Done (GPD)

## Repository structure

```text
.
├── .agents/
│   └── skills/
├── .codex/
│   ├── agents/
│   ├── get-physics-done/
│   │   ├── references/
│   │   ├── templates/
│   │   └── workflows/
│   └── hooks/
├── .github/
│   ├── ISSUE_TEMPLATE/
│   └── workflows/
├── .gpd/
│   ├── observability/
│   ├── phases/
│   │   └── 01-overnight-paper-run/
│   └── traces/
├── configs/
├── dev/
├── docs/
├── paper_runs/
│   └── fusion_transport_paper_001/
│       ├── 00_scope/
│       ├── 01_sources/
│       ├── 02_claims/
│       ├── 03_disagreements/
│       ├── 04_model/
│       ├── 05_outline/
│       ├── 06_sections/
│       ├── 07_revision/
│       ├── 08_figures/
│       └── 09_final/
├── runs/
│   └── security/
├── scripts/
├── src/
│   ├── gpd_test/
│   └── scripts/
├── tests/
├── .gitignore
├── LICENSE
├── Makefile
├── PLAN.md
├── README.md
├── pyproject.toml
├── run_config.yaml
├── security_best_practices_report.md
└── uv.lock
```

### Structure notes

- `paper_runs/` holds the generated research artifacts for each bounded overnight run.
- `.gpd/` stores GPD project state, plans, traces, and research workflow metadata.
- `.codex/` contains Codex agents, hooks, and the vendored GPD reference/workflow material used by this repo.
- `src/` and `tests/` contain the small Python support code and its verification suite.
- `.github/workflows/` defines CI, CodeQL, and supply-chain/security automation.
