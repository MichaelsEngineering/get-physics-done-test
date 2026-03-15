from pathlib import Path


def main() -> int:
    required = [
        Path(".venv"),
        Path("pyproject.toml"),
        Path(".codex/config.toml"),
        Path("PLAN.md"),
        Path("run_config.yaml"),
    ]
    missing = [str(p) for p in required if not p.exists()]
    if missing:
        print("Missing:", ", ".join(missing))
        return 1
    print("Environment OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
