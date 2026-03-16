from __future__ import annotations

import json
import re
import subprocess
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Iterable

import tomllib


HEX_SHA_RE = re.compile(r"^[0-9a-f]{40}$")
USES_RE = re.compile(r"^\s*-\s*uses:\s*([^\s@]+)@([^\s]+)\s*$")
SECRET_PATTERNS: tuple[tuple[str, re.Pattern[str]], ...] = (
    ("github_token", re.compile(r"\bgh[pousr]_[A-Za-z0-9]{20,}\b")),
    ("github_pat", re.compile(r"\bgithub_pat_[A-Za-z0-9_]{20,}\b")),
    ("aws_access_key", re.compile(r"\bAKIA[0-9A-Z]{16}\b")),
    ("private_key", re.compile(r"-----BEGIN (?:RSA|EC|OPENSSH|DSA) PRIVATE KEY-----")),
    (
        "generic_secret",
        re.compile(r"(?i)\b(?:api[_-]?key|secret|token|password)\b\s*[:=]\s*['\"][^'\"]{8,}['\"]"),
    ),
)
VOLATILE_PATH_PREFIXES = (
    ".gpd/observability/",
    ".gpd/traces/",
)
VOLATILE_FILE_NAMES = {
    ".gpd/state.json",
    ".gpd/config.json",
}
REQUIRED_IGNORE_ENTRIES = {
    ".gpd/observability/",
    ".gpd/traces/",
    ".gpd/state.json",
    ".gpd/config.json",
    "paper_runs/",
    "runs/",
    "*.aux",
    "*.log",
    "*.out",
    "*.pdf",
}
SBOM_PATH = Path("runs/security/sbom.cdx.json")


def _iter_files(root: Path) -> Iterable[Path]:
    ignored_dirs = {".git", ".venv", "__pycache__", ".pytest_cache", ".mypy_cache", ".ruff_cache"}
    for path in root.rglob("*"):
        if any(part in ignored_dirs for part in path.parts):
            continue
        if path.is_file():
            yield path


def _iter_tracked_files(root: Path) -> Iterable[Path]:
    try:
        result = subprocess.run(
            ["git", "ls-files"],
            cwd=root,
            check=True,
            capture_output=True,
            text=True,
        )
    except (OSError, subprocess.CalledProcessError):
        yield from _iter_files(root)
        return

    for line in result.stdout.splitlines():
        if not line:
            continue
        path = root / line
        if path.is_file():
            yield path


def _read_text(path: Path) -> str | None:
    try:
        return path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        return None


def _check_action_pins(root: Path) -> list[str]:
    errors: list[str] = []
    workflows = root / ".github" / "workflows"
    if not workflows.exists():
        return errors

    for workflow in sorted(workflows.glob("*.y*ml")):
        text = _read_text(workflow)
        if text is None:
            errors.append(f"unable to read workflow: {workflow}")
            continue
        for lineno, line in enumerate(text.splitlines(), start=1):
            match = USES_RE.match(line)
            if not match:
                continue
            action, ref = match.groups()
            if action.startswith("./"):
                continue
            if not HEX_SHA_RE.fullmatch(ref):
                rel = workflow.relative_to(root)
                errors.append(f"{rel}:{lineno} uses mutable action ref {action}@{ref}")
    return errors


def _check_ignore_entries(root: Path) -> list[str]:
    gitignore = root / ".gitignore"
    text = _read_text(gitignore) or ""
    entries = {
        line.strip() for line in text.splitlines() if line.strip() and not line.startswith("#")
    }
    missing = sorted(REQUIRED_IGNORE_ENTRIES - entries)
    return [f".gitignore missing entry: {entry}" for entry in missing]


def _scan_for_secrets(root: Path) -> list[str]:
    findings: list[str] = []
    skip_names = {"security_best_practices_report.md", "uv.lock"}
    skip_suffixes = {".pdf", ".png", ".svg"}

    for path in _iter_tracked_files(root):
        rel = path.relative_to(root)
        rel_str = rel.as_posix()
        if path.name in skip_names or path.suffix in skip_suffixes:
            continue
        text = _read_text(path)
        if text is None:
            continue
        for lineno, line in enumerate(text.splitlines(), start=1):
            for label, pattern in SECRET_PATTERNS:
                if pattern.search(line):
                    findings.append(f"{rel_str}:{lineno} matched {label}")
    return findings


def _scan_for_volatile_files(root: Path) -> list[str]:
    findings: list[str] = []
    for path in _iter_tracked_files(root):
        rel = path.relative_to(root).as_posix()
        if rel in VOLATILE_FILE_NAMES or rel.startswith(VOLATILE_PATH_PREFIXES):
            findings.append(rel)
    return findings


def _parse_dependency_name(raw: str) -> str:
    token = re.split(r"[<>=!~; ]", raw, maxsplit=1)[0]
    return token.split("[", 1)[0]


def _load_pyproject(root: Path) -> dict[str, object]:
    with (root / "pyproject.toml").open("rb") as handle:
        data = tomllib.load(handle)
    if not isinstance(data, dict):
        raise ValueError("pyproject.toml must contain a table at the top level")
    return data


def _build_components(
    project: dict[str, object], dependency_groups: dict[str, object]
) -> list[dict[str, str]]:
    components: list[dict[str, str]] = []

    dependencies = project.get("dependencies", [])
    if isinstance(dependencies, list):
        for dep in dependencies:
            if isinstance(dep, str):
                components.append(
                    {
                        "type": "library",
                        "name": _parse_dependency_name(dep),
                        "scope": "required",
                        "version": dep,
                    }
                )

    dev_dependencies = dependency_groups.get("dev", [])
    if isinstance(dev_dependencies, list):
        for dep in dev_dependencies:
            if isinstance(dep, str):
                components.append(
                    {
                        "type": "library",
                        "name": _parse_dependency_name(dep),
                        "scope": "optional",
                        "version": dep,
                    }
                )

    unique: dict[tuple[str, str], dict[str, str]] = {}
    for component in components:
        key = (component["name"], component["scope"])
        unique[key] = component
    return list(unique.values())


def generate_sbom(root: Path) -> Path:
    pyproject = _load_pyproject(root)
    project = pyproject.get("project", {})
    dependency_groups = pyproject.get("dependency-groups", {})
    if not isinstance(project, dict) or not isinstance(dependency_groups, dict):
        raise ValueError("invalid pyproject dependency layout")

    metadata = {
        "timestamp": datetime.now(UTC).isoformat(),
        "component": {
            "type": "application",
            "name": str(project.get("name", "unknown")),
            "version": str(project.get("version", "0.0.0")),
        },
    }
    bom = {
        "bomFormat": "CycloneDX",
        "specVersion": "1.5",
        "version": 1,
        "metadata": metadata,
        "components": _build_components(project, dependency_groups),
    }

    output_path = root / SBOM_PATH
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(bom, indent=2, sort_keys=True), encoding="utf-8")
    return output_path


def run_gate(root: Path) -> list[str]:
    errors = _check_ignore_entries(root)
    errors.extend(_check_action_pins(root))
    return errors


def run_audit(root: Path) -> list[str]:
    errors = run_gate(root)
    errors.extend(
        f"volatile file present in repo tree: {path}" for path in _scan_for_volatile_files(root)
    )
    errors.extend(
        f"potential secret pattern found: {finding}" for finding in _scan_for_secrets(root)
    )
    return errors


def main(argv: list[str] | None = None) -> int:
    args = argv if argv is not None else sys.argv[1:]
    command = args[0] if args else "gate"
    root = Path.cwd()

    if command == "gate":
        errors = run_gate(root)
        if errors:
            print("\n".join(errors))
            return 1
        print("Security gate OK")
        return 0

    if command == "audit":
        errors = run_audit(root)
        if errors:
            print("\n".join(errors))
            return 1
        print("Security audit OK")
        return 0

    if command == "sbom":
        output_path = generate_sbom(root)
        print(output_path.as_posix())
        return 0

    print(f"unknown command: {command}", file=sys.stderr)
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
