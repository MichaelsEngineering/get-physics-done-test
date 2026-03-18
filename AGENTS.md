# Repository Workflow Guide

This repository is a GPD-compatible simulation workspace. Preserve the existing research and workflow structure under `.gpd/`, `.codex/`, `paper_runs/`, and the support tooling in `src/scripts/` while editing the simulation package under `src/sentinel_core/` and tests under `tests/`.

## Required local workflow

Use the repo-local environment and tools. Prefer `uv` and `.venv`-backed commands over assuming globally installed Python tooling.

Canonical setup:

```bash
uv sync --dev
```

Before finishing any code change, run:

```bash
make format
make check
```

The `Makefile` is expected to run through the repo environment via `uv run`, so these targets should work from a fresh shell without manual activation.

The `make check` target intentionally includes a non-mutating Ruff format check. If it fails with output like `Would reformat: ...`, that means files were edited without being formatted first. Treat this as a workflow issue, not a lint policy bug:

```bash
make format
make check
```

For partial edits, it is acceptable to format only the changed files first and then run the full gate:

```bash
.venv/bin/ruff format <changed files>
make check
```

## Editing guidance

- Apply the same formatting workflow to `src/sentinel_core/`, `tests/`, and the existing GPD/support code.
- Do not edit generated or workflow state directories as part of routine code fixes unless the task explicitly requires it.
- Keep `Makefile` semantics intact unless there is a real tooling problem; `ruff format --check` should remain part of the gate.
