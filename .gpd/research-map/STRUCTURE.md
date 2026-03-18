# Project Structure

**Analysis Date:** 2026-03-18

## Directory Layout

```text
[project-root]/
+-- .gpd/                     # GPD project authority, state, roadmap, and research map
+-- .codex/get-physics-done/  # Vendored GPD references and workflows
+-- docs/                     # User-facing architecture report
+-- paper_runs/               # Historical overnight paper artifacts
+-- src/gpd_test/             # CLI entrypoint
+-- src/sentinel_core/        # Simulation package
+-- src/scripts/              # Environment and security support tooling
+-- tests/                    # Baseline verification suite
+-- PLAN.md                   # Top-level program statement
+-- README.md                 # Repo summary
+-- Makefile                  # Quality and workflow commands
+-- pyproject.toml            # Packaging and dependency metadata
```

## Directory Purposes

**`.gpd/`:**
- Purpose: authoritative GPD project map, requirements, roadmap, state, and research-map documents
- Key files: `.gpd/PROJECT.md`, `.gpd/REQUIREMENTS.md`, `.gpd/ROADMAP.md`, `.gpd/research-map/*.md`

**`src/sentinel_core/`:**
- Purpose: executable simulation and theory-chain package
- Contains: configuration, geometry, symmetry, operators, closure models, integrators, problems, reporting
- Key files: `src/sentinel_core/core.py`, `src/sentinel_core/problems/turbulence.py`

**`tests/`:**
- Purpose: executable checks for environment, security, CLI behavior, and simulation architecture
- Key files: `tests/test_simulation_architecture.py`, `tests/test_cli.py`

## Key File Locations

**Theory / Derivations:**
- `docs/architecture.md`: program spine and theory mapping
- `.gpd/research-map/FORMALISM.md`: mapped theoretical framework

**Computation / Numerics:**
- `src/sentinel_core/core.py`: task construction and rollout
- `src/sentinel_core/operators/grid.py`: grid operator
- `src/sentinel_core/integrators/sciml.py`: structure-preserving stepper

**Configuration / Parameters:**
- `src/sentinel_core/config.py`: typed task configuration
- `pyproject.toml`: dependency groups and optional extras

## Document Dependency Graph

**Program Docs:**
- `PLAN.md` informs `.gpd/PROJECT.md`
- `.gpd/PROJECT.md`, `.gpd/REQUIREMENTS.md`, and `.gpd/ROADMAP.md` define the active research contract
- `.gpd/research-map/*.md` expands the contract into formalism, structure, validation, references, and concerns

**Computation Dependencies:**
- `src/gpd_test/cli.py` calls `src/sentinel_core/cli_support.py`
- `src/sentinel_core/cli_support.py` calls `build_task()`, `run_rollout()`, and reporting functions
- `tests/test_simulation_architecture.py` verifies the same public API and rollout surface

## Naming Conventions

**Files:**
- `src/sentinel_core/[subsystem]/[concept].py`
- `.gpd/research-map/[DOCUMENT].md`

**Variables in Code:**
- Geometry, symmetry, operator, closure, and integrator objects use physics-role names instead of framework names

## Where to Add New Content

**New benchmark problem:**
- Implementation: `src/sentinel_core/problems/`
- Task wiring: `src/sentinel_core/core.py`
- Tests: `tests/test_simulation_architecture.py` or a dedicated benchmark test file

**New validation protocol:**
- Research docs: `.gpd/research-map/VALIDATION.md`
- Tests or benchmark harness: `tests/` plus future scripts under `src/sentinel_core/`

**New paper candidate:**
- Add evidence path and claim structure to `.gpd/research-map/PAPER_OUTLINES.md`

## Build and Execution

**Environment setup:**

```bash
uv sync --dev
```

**Run tests:**

```bash
.venv/bin/pytest -q
```

**Run CLI smoke commands:**

```bash
.venv/bin/python -m src.gpd_test.cli smoke-grid --steps 2
.venv/bin/python -m src.gpd_test.cli architecture
```

---

_Structure analysis: 2026-03-18_
