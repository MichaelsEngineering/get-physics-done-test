from __future__ import annotations

import json

from typer.testing import CliRunner

from src.gpd_test.cli import app


runner = CliRunner()


def test_architecture_command_returns_requested_sections() -> None:
    result = runner.invoke(app, ["architecture"])

    assert result.exit_code == 0
    assert "architecture summary" in result.stdout
    assert "file tree" in result.stdout
    assert "theory mapping" in result.stdout


def test_smoke_grid_command_returns_rollout_summary() -> None:
    result = runner.invoke(app, ["smoke-grid", "--steps", "2"])

    assert result.exit_code == 0
    payload = json.loads(result.stdout)
    assert payload["task"] == "grid_turbulence"
    assert payload["steps"] == 2
    assert payload["diagnostics"]["energy"] > 0.0


def test_file_tree_command_mentions_simulation_package() -> None:
    result = runner.invoke(app, ["file-tree"])

    assert result.exit_code == 0
    assert "src/sentinel_core/" in result.stdout
    assert "geometry/" in result.stdout
