from __future__ import annotations

import typer

from src.sentinel_core.cli_support import (
    architecture_report,
    equivariant_report,
    file_tree_report,
    graph_report,
    smoke_grid_report,
    theory_mapping_report,
    training_report,
)

app = typer.Typer(add_completion=False, no_args_is_help=True)


@app.command("architecture")
def architecture() -> None:
    print(architecture_report())


@app.command("file-tree")
def file_tree() -> None:
    print(file_tree_report())


@app.command("smoke-grid")
def smoke_grid(steps: int = 3) -> None:
    print(smoke_grid_report(steps=steps))


@app.command("theory-mapping")
def theory_mapping() -> None:
    print(theory_mapping_report())


@app.command("train-grid")
def train_grid() -> None:
    print(training_report())


@app.command("smoke-graph")
def smoke_graph() -> None:
    print(graph_report())


@app.command("smoke-equivariant")
def smoke_equivariant() -> None:
    print(equivariant_report())


def main() -> None:
    app()


if __name__ == "__main__":
    main()
