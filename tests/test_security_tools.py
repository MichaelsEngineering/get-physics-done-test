import json
from pathlib import Path

from src.scripts import security_tools


def _write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def test_run_gate_accepts_pinned_workflows_and_required_ignores(tmp_path: Path) -> None:
    _write(
        tmp_path / ".gitignore",
        "\n".join(sorted(security_tools.REQUIRED_IGNORE_ENTRIES)) + "\n",
    )
    _write(
        tmp_path / ".github" / "workflows" / "ci.yml",
        "steps:\n  - uses: actions/checkout@34e114876b0b11c390a56381ad16ebd13914f8d5\n",
    )

    assert security_tools.run_gate(tmp_path) == []


def test_run_gate_rejects_mutable_action_refs(tmp_path: Path) -> None:
    _write(
        tmp_path / ".gitignore",
        "\n".join(sorted(security_tools.REQUIRED_IGNORE_ENTRIES)) + "\n",
    )
    _write(
        tmp_path / ".github" / "workflows" / "ci.yml",
        "steps:\n  - uses: actions/checkout@v4\n",
    )

    errors = security_tools.run_gate(tmp_path)

    assert any("mutable action ref" in error for error in errors)


def test_run_audit_detects_secret_patterns(tmp_path: Path) -> None:
    _write(
        tmp_path / ".gitignore",
        "\n".join(sorted(security_tools.REQUIRED_IGNORE_ENTRIES)) + "\n",
    )
    _write(
        tmp_path / ".github" / "workflows" / "ci.yml",
        "steps:\n  - uses: actions/checkout@34e114876b0b11c390a56381ad16ebd13914f8d5\n",
    )
    token_value = "ghp_" + "123456789012345678901234567890123456"
    fixture_line = "".join(["to", "ken", ' = "', token_value, '"\n'])
    _write(tmp_path / "src" / "example.py", fixture_line)

    errors = security_tools.run_audit(tmp_path)

    assert any("potential secret pattern found" in error for error in errors)


def test_generate_sbom_writes_expected_file(tmp_path: Path) -> None:
    _write(
        tmp_path / "pyproject.toml",
        "\n".join(
            [
                "[project]",
                'name = "demo"',
                'version = "1.2.3"',
                'dependencies = ["typer>=0.12", "pyyaml>=6.0"]',
                "",
                "[dependency-groups]",
                'dev = ["pytest>=8.2"]',
            ]
        )
        + "\n",
    )

    output_path = security_tools.generate_sbom(tmp_path)
    payload = json.loads(output_path.read_text(encoding="utf-8"))

    assert output_path == tmp_path / "runs" / "security" / "sbom.cdx.json"
    assert payload["bomFormat"] == "CycloneDX"
    assert payload["metadata"]["component"]["name"] == "demo"
    names = {component["name"] for component in payload["components"]}
    assert names == {"pytest", "pyyaml", "typer"}
