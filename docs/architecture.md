# architecture summary

The repo is organized around a theory chain that makes the physics assumptions explicit instead of hiding them inside model-specific code.

- `geometry`: regular grid, graph mesh, or equivariant geometric state.
- `symmetry`: periodic translation, permutation/locality, or Euclidean equivariance.
- `operator class`: regular-grid stencil/spectral dynamics, message passing on graphs, or equivariant operators.
- `closure`: learned residual or subgrid correction constrained by the operator family.
- `integrator`: structure-preserving rollout with stability and diagnostic checks.

The first working core is periodic 2D turbulence on a regular grid. It uses a deterministic finite-difference backbone plus a neuraloperator-oriented closure approximation implemented with a lightweight local spectral-mixing surrogate. GraphCast-style graph forecasting and e3nn-style equivariant states share the same rollout contract but remain scaffold-level in this refactor.

# file tree

```text
src/sentinel_core/
├── __init__.py
├── cli_support.py
├── config.py
├── core.py
├── reporting.py
├── geometry/
│   ├── __init__.py
│   ├── equivariant.py
│   ├── graph.py
│   └── grid.py
├── symmetry/
│   ├── __init__.py
│   └── resolver.py
├── operators/
│   ├── __init__.py
│   ├── equivariant.py
│   ├── graph.py
│   └── grid.py
├── closure/
│   ├── __init__.py
│   ├── equivariant.py
│   ├── graph.py
│   └── grid.py
├── integrators/
│   ├── __init__.py
│   └── sciml.py
├── problems/
│   ├── __init__.py
│   └── turbulence.py
└── training.py
```

# full file replacements

The authoritative implementation files for this refactor are:

- `README.md`
- `pyproject.toml`
- `Makefile`
- `src/gpd_test/cli.py`
- `src/sentinel_core/**`
- `tests/test_simulation_architecture.py`
- `tests/test_cli.py`

These files define the public CLI, typed configuration chain, working grid rollout, graph/equivariant scaffolds, and the architecture report consumed by future automation.

# run commands

```bash
uv sync --dev
uv sync --dev --extra sim
uv sync --dev --extra sim --extra graph --extra equivariant
uv run gpd-test architecture
uv run gpd-test file-tree
uv run gpd-test smoke-grid
uv run gpd-test theory-mapping
make test
```

# theory mapping

- Brandstetter-style geometric deep learning provides the bridge:
  geometry defines what transformations are admissible, and those transformations define the hypothesis class.
- neuraloperator maps to the regular-grid closure/operator layer:
  the learned component acts on periodic grid states and corrects resolved dynamics without replacing the integrator.
- GraphCast informs the graph scaffold:
  encoder/processor/decoder structure, graph-local message passing, and autoregressive rollout all fit under the same `SimulationTask` contract.
- SciML principles inform the integrator:
  rollout is not just prediction, it is the place where invariants, stability checks, and physically meaningful diagnostics are enforced.
- e3nn informs the equivariant scaffold:
  feature types are tied to Euclidean transformation behavior, so equivariance is represented as a first-class state/operator concern instead of an afterthought.
