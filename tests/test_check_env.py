import json
from pathlib import Path

from src.scripts import check_env


def _write(path: Path, text: str = "") -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def _write_json(path: Path, payload: dict) -> None:
    _write(path, json.dumps(payload, indent=2))


def _base_run_config(run_id: str = "fusion_transport_paper_001") -> str:
    return "\n".join(
        [
            f"run_id: {run_id}",
            'start_time_local: "2026-03-15T23:00:00"',
            'freeze_new_research_local: "2026-03-16T03:00:00"',
            'hard_stop_local: "2026-03-16T04:00:00"',
            "limits:",
            "  max_runtime_minutes: 300",
            "required_outputs:",
            f"  - paper_runs/{run_id}/trace.json",
            f"  - paper_runs/{run_id}/01_sources/paper_summaries.md",
            f"  - paper_runs/{run_id}/02_claims/claims_table.csv",
            f"  - paper_runs/{run_id}/03_disagreements/disagreement_map.md",
            f"  - paper_runs/{run_id}/05_outline/paper_outline.md",
            f"  - paper_runs/{run_id}/09_final/final_paper.md",
            f"  - paper_runs/{run_id}/09_final/executive_summary.md",
        ]
    )


def _base_trace(status: str = "in_progress", stage_statuses: list[str] | None = None) -> dict:
    statuses = stage_statuses or ["complete", "pending", "pending"]
    return {
        "run_id": "fusion_transport_paper_001",
        "status": status,
        "stages": [
            {"name": "sources-and-claims", "status": statuses[0]},
            {"name": "draft-and-figures", "status": statuses[1]},
            {"name": "revision-and-final-assembly", "status": statuses[2]},
        ],
    }


def _seed_repo_scaffold(root: Path) -> None:
    (root / ".venv").mkdir()
    _write(root / "pyproject.toml", "[project]\nname='test'\n")
    _write(root / ".codex" / "config.toml", "")
    _write(root / "PLAN.md", "# plan\n")
    _write(root / ".gpd" / "PROJECT.md", "# project\n")
    _write(root / ".gpd" / "ROADMAP.md", "# roadmap\n")
    _write(
        root / ".gpd" / "STATE.md",
        "\n".join(
            [
                "# Research State",
                "",
                "**Resume file:** `.gpd/phases/01-overnight-paper-run/01-01-PLAN.md`",
            ]
        ),
    )
    _write_json(
        root / ".gpd" / "state.json",
        {"session": {"resume_file": ".gpd/phases/01-overnight-paper-run/01-01-PLAN.md"}},
    )
    _write(root / ".gpd" / "config.json", "{}")
    (root / ".gpd" / "phases").mkdir(parents=True)
    _write(root / "run_config.yaml", _base_run_config())


def _create_stage_one_outputs(root: Path) -> None:
    run_root = root / "paper_runs" / "fusion_transport_paper_001"
    _write(run_root / "01_sources" / "paper_summaries.md", "")
    _write(run_root / "02_claims" / "claims_table.csv", "")
    _write(run_root / "03_disagreements" / "disagreement_map.md", "")
    _write(run_root / "05_outline" / "paper_outline.md", "")


def _create_partial_sections(root: Path) -> None:
    run_root = root / "paper_runs" / "fusion_transport_paper_001"
    _write(run_root / "06_sections" / "01_introduction.md", "")
    _write(run_root / "06_sections" / "02_background.md", "")


def _create_complete_run(root: Path) -> None:
    run_root = root / "paper_runs" / "fusion_transport_paper_001"
    _create_stage_one_outputs(root)
    for name in [
        "01_introduction.md",
        "02_background.md",
        "03_field_disagreement.md",
        "04_thesis.md",
        "05_method_or_framework.md",
        "06_commercial_relevance.md",
        "07_risks_limitations.md",
        "08_conclusion.md",
    ]:
        _write(run_root / "06_sections" / name, "")
    _write(run_root / "07_revision" / "critic_report.md", "")
    _write(run_root / "07_revision" / "revision_plan.md", "")
    _write(run_root / "09_final" / "final_paper.md", "")
    _write(run_root / "09_final" / "executive_summary.md", "")
    _write_json(
        run_root / "trace.json",
        _base_trace(status="complete", stage_statuses=["complete", "complete", "complete"]),
    )
    _write(
        root / ".gpd" / "STATE.md",
        "# Research State\n\n**Resume file:** `.gpd/phases/01-overnight-paper-run/01-03-PLAN.md`\n",
    )
    _write_json(
        root / ".gpd" / "state.json",
        {"session": {"resume_file": ".gpd/phases/01-overnight-paper-run/01-03-PLAN.md"}},
    )


def test_validate_run_config_accepts_consistent_window(tmp_path: Path) -> None:
    path = tmp_path / "run_config.yaml"
    path.write_text(_base_run_config("demo"), encoding="utf-8")

    assert check_env._validate_run_config(path) == []


def test_validate_run_config_rejects_inverted_window(tmp_path: Path) -> None:
    path = tmp_path / "run_config.yaml"
    path.write_text(
        "\n".join(
            [
                "run_id: demo",
                'start_time_local: "2026-03-15T23:00:00"',
                'freeze_new_research_local: "2026-03-16T04:45:00"',
                'hard_stop_local: "2026-03-16T03:45:00"',
                "required_outputs:",
                "  - paper_runs/demo/trace.json",
                "limits:",
                "  max_runtime_minutes: 300",
            ]
        ),
        encoding="utf-8",
    )

    errors = check_env._validate_run_config(path)

    assert "freeze_new_research_local must be earlier than hard_stop_local" in errors


def test_validate_run_config_rejects_runtime_mismatch(tmp_path: Path) -> None:
    path = tmp_path / "run_config.yaml"
    path.write_text(
        "\n".join(
            [
                "run_id: demo",
                'start_time_local: "2026-03-15T23:00:00"',
                'freeze_new_research_local: "2026-03-16T03:00:00"',
                'hard_stop_local: "2026-03-16T04:00:00"',
                "required_outputs:",
                "  - paper_runs/demo/trace.json",
                "limits:",
                "  max_runtime_minutes: 405",
            ]
        ),
        encoding="utf-8",
    )

    errors = check_env._validate_run_config(path)

    assert any("must match the start/hard stop window" in error for error in errors)


def test_validate_run_config_requires_required_outputs(tmp_path: Path) -> None:
    path = tmp_path / "run_config.yaml"
    path.write_text(
        "\n".join(
            [
                "run_id: demo",
                'start_time_local: "2026-03-15T23:00:00"',
                'freeze_new_research_local: "2026-03-16T03:00:00"',
                'hard_stop_local: "2026-03-16T04:00:00"',
                "limits:",
                "  max_runtime_minutes: 300",
            ]
        ),
        encoding="utf-8",
    )

    assert "run_config missing: required_outputs" in check_env._validate_run_config(path)


def test_inspect_run_state_reports_not_started(tmp_path: Path) -> None:
    _seed_repo_scaffold(tmp_path)

    report = check_env.inspect_run_state(tmp_path)

    assert report["status"] == "not_started"
    assert report["recommended_plan"] == 1


def test_inspect_run_state_reports_interrupted_after_stage_one(tmp_path: Path) -> None:
    _seed_repo_scaffold(tmp_path)
    _create_stage_one_outputs(tmp_path)
    _write_json(
        tmp_path / "paper_runs" / "fusion_transport_paper_001" / "trace.json", _base_trace()
    )

    report = check_env.inspect_run_state(tmp_path)

    assert report["status"] == "inconsistent"
    assert report["recommended_plan"] == 2
    assert report["recommended_resume_file"].endswith("01-02-PLAN.md")
    assert "resume hint conflicts with detected recovery point" in "\n".join(report["errors"])


def test_inspect_run_state_reports_partial_section_drafting(tmp_path: Path) -> None:
    _seed_repo_scaffold(tmp_path)
    _create_stage_one_outputs(tmp_path)
    _create_partial_sections(tmp_path)
    _write_json(
        tmp_path / "paper_runs" / "fusion_transport_paper_001" / "trace.json", _base_trace()
    )

    report = check_env.inspect_run_state(tmp_path)

    assert report["status"] == "inconsistent"
    assert report["recommended_plan"] == 3
    assert report["first_incomplete_stage"] == "draft-and-figures"
    assert any(
        path.endswith("09_final/final_paper.md") for path in report["missing_required_outputs"]
    )


def test_inspect_run_state_reports_missing_final_outputs_with_complete_trace(
    tmp_path: Path,
) -> None:
    _seed_repo_scaffold(tmp_path)
    _create_stage_one_outputs(tmp_path)
    _create_partial_sections(tmp_path)
    _write_json(
        tmp_path / "paper_runs" / "fusion_transport_paper_001" / "trace.json",
        _base_trace(status="complete", stage_statuses=["complete", "complete", "complete"]),
    )
    _write(
        tmp_path / ".gpd" / "STATE.md",
        "# Research State\n\n**Resume file:** `.gpd/phases/01-overnight-paper-run/01-03-PLAN.md`\n",
    )
    _write_json(
        tmp_path / ".gpd" / "state.json",
        {"session": {"resume_file": ".gpd/phases/01-overnight-paper-run/01-03-PLAN.md"}},
    )

    report = check_env.inspect_run_state(tmp_path)

    assert report["status"] == "inconsistent"
    assert report["recommended_plan"] == 3
    assert "trace.json marks the run complete but required outputs are missing" in "\n".join(
        report["errors"]
    )


def test_inspect_run_state_reports_missing_trace_with_partial_artifacts(tmp_path: Path) -> None:
    _seed_repo_scaffold(tmp_path)
    _create_stage_one_outputs(tmp_path)
    _create_partial_sections(tmp_path)

    report = check_env.inspect_run_state(tmp_path)

    assert report["status"] == "inconsistent"
    assert report["recommended_plan"] == 3
    assert "run artifacts exist but trace.json is missing" in "\n".join(report["errors"])


def test_inspect_run_state_reports_conflicting_resume_hint(tmp_path: Path) -> None:
    _seed_repo_scaffold(tmp_path)
    _create_stage_one_outputs(tmp_path)
    _write_json(
        tmp_path / "paper_runs" / "fusion_transport_paper_001" / "trace.json", _base_trace()
    )
    _write(
        tmp_path / ".gpd" / "STATE.md",
        "# Research State\n\n**Resume file:** `.gpd/phases/01-overnight-paper-run/01-03-PLAN.md`\n",
    )
    _write_json(
        tmp_path / ".gpd" / "state.json",
        {"session": {"resume_file": ".gpd/phases/01-overnight-paper-run/01-03-PLAN.md"}},
    )

    report = check_env.inspect_run_state(tmp_path)

    assert report["status"] == "inconsistent"
    assert "resume hint conflicts with detected recovery point" in "\n".join(report["errors"])


def test_inspect_run_state_accepts_clean_complete_run(tmp_path: Path) -> None:
    _seed_repo_scaffold(tmp_path)
    _create_complete_run(tmp_path)

    report = check_env.inspect_run_state(tmp_path)

    assert report["status"] == "complete"
    assert report["recommended_plan"] == 3


def test_recover_main_exits_nonzero_for_interrupted_run(
    tmp_path: Path, monkeypatch, capsys
) -> None:
    _seed_repo_scaffold(tmp_path)
    _create_stage_one_outputs(tmp_path)
    _create_partial_sections(tmp_path)
    _write_json(
        tmp_path / "paper_runs" / "fusion_transport_paper_001" / "trace.json", _base_trace()
    )
    monkeypatch.chdir(tmp_path)

    code = check_env.recover_main()
    output = capsys.readouterr().out

    assert code == 1
    assert "Recommended resume file: .gpd/phases/01-overnight-paper-run/01-03-PLAN.md" in output
    assert "Status: inconsistent" in output


def test_main_passes_for_complete_run(tmp_path: Path, monkeypatch, capsys) -> None:
    _seed_repo_scaffold(tmp_path)
    _create_complete_run(tmp_path)
    monkeypatch.chdir(tmp_path)

    code = check_env.main()
    output = capsys.readouterr().out

    assert code == 0
    assert "Environment OK" in output


def test_main_fails_for_partial_run(tmp_path: Path, monkeypatch, capsys) -> None:
    _seed_repo_scaffold(tmp_path)
    _create_stage_one_outputs(tmp_path)
    _create_partial_sections(tmp_path)
    _write_json(
        tmp_path / "paper_runs" / "fusion_transport_paper_001" / "trace.json", _base_trace()
    )
    monkeypatch.chdir(tmp_path)

    code = check_env.main()
    output = capsys.readouterr().out

    assert code == 1
    assert "Recommended resume file: .gpd/phases/01-overnight-paper-run/01-03-PLAN.md" in output
