from __future__ import annotations

import json
import re
import sys
from datetime import datetime
from pathlib import Path
from typing import Any

import yaml


def _parse_local_timestamp(value: object) -> datetime:
    if not isinstance(value, str):
        raise ValueError(f"expected timestamp string, got {type(value).__name__}")
    return datetime.fromisoformat(value)


def _load_run_config(path: Path) -> dict[str, object]:
    with path.open("r", encoding="utf-8") as handle:
        data = yaml.safe_load(handle) or {}
    if not isinstance(data, dict):
        raise ValueError("run_config.yaml must contain a mapping at the top level")
    return data


def _validate_run_config(run_config_path: Path) -> list[str]:
    errors: list[str] = []
    try:
        config = _load_run_config(run_config_path)
    except (OSError, ValueError, yaml.YAMLError) as exc:
        return [f"invalid run_config.yaml: {exc}"]

    for key in ("run_id", "start_time_local", "freeze_new_research_local", "hard_stop_local"):
        if key not in config:
            errors.append(f"run_config missing: {key}")

    required_outputs = config.get("required_outputs")
    if required_outputs is None:
        errors.append("run_config missing: required_outputs")
    elif not isinstance(required_outputs, list) or not all(
        isinstance(output, str) for output in required_outputs
    ):
        errors.append("run_config.required_outputs must be a list of strings")

    if errors:
        return errors

    try:
        start = _parse_local_timestamp(config["start_time_local"])
        freeze = _parse_local_timestamp(config["freeze_new_research_local"])
        hard_stop = _parse_local_timestamp(config["hard_stop_local"])
    except ValueError as exc:
        return [f"invalid run_config timestamp: {exc}"]

    if not start < freeze:
        errors.append("start_time_local must be earlier than freeze_new_research_local")
    if not freeze < hard_stop:
        errors.append("freeze_new_research_local must be earlier than hard_stop_local")

    limits = config.get("limits", {})
    if isinstance(limits, dict) and "max_runtime_minutes" in limits:
        max_runtime = limits["max_runtime_minutes"]
        if not isinstance(max_runtime, int):
            errors.append("limits.max_runtime_minutes must be an integer")
        else:
            actual_minutes = int((hard_stop - start).total_seconds() // 60)
            if max_runtime != actual_minutes:
                errors.append(
                    "limits.max_runtime_minutes must match the start/hard stop window "
                    f"({actual_minutes} minutes)"
                )

    return errors


def _load_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        data = json.load(handle)
    if not isinstance(data, dict):
        raise ValueError(f"{path} must contain a JSON object at the top level")
    return data


def _load_optional_json(path: Path) -> dict[str, Any] | None:
    if not path.exists():
        return None
    try:
        return _load_json(path)
    except (OSError, ValueError, json.JSONDecodeError):
        return None


def _extract_resume_file_from_state_md(path: Path) -> str | None:
    if not path.exists():
        return None
    match = re.search(r"^\*\*Resume file:\*\*\s+`([^`]+)`", path.read_text(encoding="utf-8"), re.M)
    if match:
        return match.group(1)
    return None


def _load_resume_hints(root: Path) -> list[str]:
    hints: list[str] = []
    state_json = _load_optional_json(root / ".gpd" / "state.json")
    if state_json is not None:
        direct_hint = state_json.get("resume_file")
        if isinstance(direct_hint, str) and direct_hint:
            hints.append(direct_hint)
        session = state_json.get("session")
        if isinstance(session, dict):
            session_hint = session.get("resume_file")
            if isinstance(session_hint, str) and session_hint:
                hints.append(session_hint)
    state_md_hint = _extract_resume_file_from_state_md(root / ".gpd" / "STATE.md")
    if state_md_hint:
        hints.append(state_md_hint)
    return list(dict.fromkeys(hints))


def _expected_plan_file(plan_number: int) -> str:
    return f".gpd/phases/01-overnight-paper-run/01-0{plan_number}-PLAN.md"


def _detect_resume_plan(root: Path, config: dict[str, object]) -> int:
    run_id = config.get("run_id")
    if not isinstance(run_id, str) or not run_id:
        return 1

    run_root = root / "paper_runs" / run_id
    if not run_root.exists():
        return 1

    final_outputs = [
        run_root / "09_final" / "final_paper.md",
        run_root / "09_final" / "executive_summary.md",
    ]
    revision_outputs = [
        run_root / "07_revision" / "critic_report.md",
        run_root / "07_revision" / "revision_plan.md",
    ]
    section_files = [
        run_root / "06_sections" / "01_introduction.md",
        run_root / "06_sections" / "02_background.md",
        run_root / "06_sections" / "03_field_disagreement.md",
        run_root / "06_sections" / "04_thesis.md",
        run_root / "06_sections" / "05_method_or_framework.md",
        run_root / "06_sections" / "06_commercial_relevance.md",
        run_root / "06_sections" / "07_risks_limitations.md",
        run_root / "06_sections" / "08_conclusion.md",
    ]
    stage_one_outputs = [
        run_root / "01_sources" / "paper_summaries.md",
        run_root / "02_claims" / "claims_table.csv",
        run_root / "03_disagreements" / "disagreement_map.md",
        run_root / "05_outline" / "paper_outline.md",
    ]

    if any(path.exists() for path in final_outputs + revision_outputs):
        return 3
    if any(path.exists() for path in section_files):
        return 3
    if any(path.exists() for path in stage_one_outputs):
        return 2
    return 1


def _summarize_stage_statuses(trace_data: dict[str, Any] | None) -> tuple[str | None, str | None]:
    if trace_data is None:
        return None, None
    stages = trace_data.get("stages")
    if not isinstance(stages, list):
        return None, None

    latest_completed: str | None = None
    first_incomplete: str | None = None
    for stage in stages:
        if not isinstance(stage, dict):
            continue
        name = stage.get("name")
        status = stage.get("status")
        if not isinstance(name, str) or not isinstance(status, str):
            continue
        if status == "complete":
            latest_completed = name
        elif first_incomplete is None and status in {"pending", "in_progress"}:
            first_incomplete = name
    return latest_completed, first_incomplete


def inspect_run_state(root: Path | None = None) -> dict[str, Any]:
    repo_root = root or Path.cwd()
    run_config_path = repo_root / "run_config.yaml"
    config_errors = _validate_run_config(run_config_path)
    if config_errors:
        return {
            "run_id": None,
            "status": "inconsistent",
            "errors": config_errors,
            "missing_required_outputs": [],
            "latest_completed_stage": None,
            "first_incomplete_stage": None,
            "recommended_plan": None,
            "recommended_resume_file": None,
            "resume_hints": _load_resume_hints(repo_root),
            "next_action": None,
        }

    config = _load_run_config(run_config_path)
    run_id = config["run_id"]
    assert isinstance(run_id, str)
    run_root = repo_root / "paper_runs" / run_id
    required_output_values = config.get("required_outputs", [])
    assert isinstance(required_output_values, list)
    required_outputs = [
        repo_root / output for output in required_output_values if isinstance(output, str)
    ]
    missing_required_outputs = [
        str(path.relative_to(repo_root)) for path in required_outputs if not path.exists()
    ]
    trace_path = run_root / "trace.json"
    trace_data = _load_optional_json(trace_path)
    resume_hints = _load_resume_hints(repo_root)
    recommended_plan = _detect_resume_plan(repo_root, config)
    recommended_resume_file = _expected_plan_file(recommended_plan)
    latest_completed_stage, first_incomplete_stage = _summarize_stage_statuses(trace_data)

    any_required_present = any(path.exists() for path in required_outputs)
    any_run_artifacts = run_root.exists() and any(run_root.rglob("*"))
    errors: list[str] = []

    if trace_path.exists() and trace_data is None:
        errors.append(f"invalid trace.json: {trace_path}")

    if any_run_artifacts and not trace_path.exists():
        errors.append("run artifacts exist but trace.json is missing")

    if trace_data is not None:
        trace_status = trace_data.get("status")
        if trace_status == "complete" and missing_required_outputs:
            errors.append("trace.json marks the run complete but required outputs are missing")
        if trace_status in {"in_progress", "pending"} and not missing_required_outputs:
            errors.append("trace.json marks the run incomplete but all required outputs exist")

    expected_resume_file = recommended_resume_file
    conflicting_hints = [hint for hint in resume_hints if hint != expected_resume_file]
    has_incomplete_signals = bool(missing_required_outputs or first_incomplete_stage is not None)
    if conflicting_hints and has_incomplete_signals:
        errors.append(
            "resume hint conflicts with detected recovery point: " + ", ".join(conflicting_hints)
        )

    if errors:
        status = "inconsistent"
    elif not any_required_present and not any_run_artifacts:
        status = "not_started"
    elif (
        not missing_required_outputs
        and trace_data is not None
        and trace_data.get("status") == "complete"
    ):
        status = "complete"
    elif missing_required_outputs or first_incomplete_stage is not None:
        status = "incomplete"
    else:
        status = "incomplete"

    next_action = None
    if status in {"incomplete", "inconsistent"}:
        if recommended_plan == 3:
            next_action = (
                f"required final outputs missing under {run_root / '09_final'}; "
                "continue final assembly stage"
            )
        elif recommended_plan == 2:
            next_action = "required section outputs are incomplete; continue drafting stage"
        else:
            next_action = (
                "required source and claims outputs are incomplete; continue initial run stage"
            )

    return {
        "run_id": run_id,
        "status": status,
        "errors": errors,
        "missing_required_outputs": missing_required_outputs,
        "latest_completed_stage": latest_completed_stage,
        "first_incomplete_stage": first_incomplete_stage,
        "recommended_plan": recommended_plan,
        "recommended_resume_file": recommended_resume_file,
        "resume_hints": resume_hints,
        "next_action": next_action,
    }


def format_recovery_report(report: dict[str, Any]) -> str:
    lines = [
        f"Run ID: {report['run_id'] or 'unknown'}",
        f"Status: {report['status']}",
    ]

    errors = report.get("errors", [])
    if errors:
        lines.append("Errors:")
        lines.extend(f"- {error}" for error in errors)

    missing = report.get("missing_required_outputs", [])
    if missing:
        lines.append("Missing required outputs:")
        lines.extend(f"- {path}" for path in missing)

    if report.get("latest_completed_stage"):
        lines.append(f"Latest completed stage: {report['latest_completed_stage']}")
    if report.get("first_incomplete_stage"):
        lines.append(f"First incomplete stage: {report['first_incomplete_stage']}")

    if report.get("recommended_resume_file"):
        lines.append(f"Recommended resume file: {report['recommended_resume_file']}")
    if report.get("recommended_plan") is not None:
        lines.append(f"Recommended resume plan: 0{report['recommended_plan']}")

    if report.get("next_action"):
        lines.append(f"Next action: {report['next_action']}")

    if report.get("status") in {"incomplete", "inconsistent"}:
        lines.append(
            "Resume command: "
            f"/home/qol/.gpd/venv/bin/python -m gpd.runtime_cli --runtime codex "
            f"--config-dir ./.codex --install-scope local init phase-op "
            f"&& resume from `{report['recommended_resume_file']}`"
        )

    return "\n".join(lines)


def recover_main() -> int:
    report = inspect_run_state()
    print(format_recovery_report(report))
    return 0 if report["status"] in {"complete", "not_started"} else 1


def main() -> int:
    required = [
        Path(".venv"),
        Path("pyproject.toml"),
        Path(".codex/config.toml"),
        Path("PLAN.md"),
        Path("run_config.yaml"),
        Path(".gpd/PROJECT.md"),
        Path(".gpd/ROADMAP.md"),
        Path(".gpd/STATE.md"),
        Path(".gpd/state.json"),
        Path(".gpd/config.json"),
        Path(".gpd/phases"),
    ]
    missing = [str(p) for p in required if not p.exists()]
    errors = []
    if missing:
        errors.append("Missing: " + ", ".join(missing))

    if not missing:
        errors.extend(_validate_run_config(Path("run_config.yaml")))
        report = inspect_run_state()
        if report["status"] in {"incomplete", "inconsistent"}:
            errors.append(format_recovery_report(report))

    if errors:
        print("\n".join(errors))
        return 1
    print("Environment OK")
    return 0


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "recover":
        raise SystemExit(recover_main())
    raise SystemExit(main())
