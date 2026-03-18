from __future__ import annotations

from pathlib import Path


DOC_PATH = Path(__file__).resolve().parents[2] / "docs" / "architecture.md"
PACKAGE_ROOT = Path(__file__).resolve().parent


def describe_architecture() -> str:
    return DOC_PATH.read_text(encoding="utf-8")


def package_file_tree() -> str:
    lines = ["src/sentinel_core/"]
    for path in sorted(PACKAGE_ROOT.rglob("*")):
        if path.name == "__pycache__":
            continue
        rel = path.relative_to(PACKAGE_ROOT)
        depth = len(rel.parts)
        prefix = "    " * (depth - 1) + "|-- "
        suffix = "/" if path.is_dir() else ""
        lines.append(f"{prefix}{rel.name}{suffix}")
    return "\n".join(lines)


def theory_mapping() -> str:
    return "\n".join(
        [
            "geometry -> grid/graph/equivariant state layout",
            "symmetry -> periodic translation / permutation locality / Euclidean equivariance",
            "operator class -> differential stencil / autoregressive message passing / equivariant tensor map",
            "closure -> neuraloperator-style residual / graph residual head / equivariant residual head",
            "integrator -> SciML structure-preserving rollout",
            "theory bridge -> Brandstetter geometric deep learning",
        ]
    )
