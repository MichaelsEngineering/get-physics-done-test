# ==== Configuration ====
PYTHON ?= python
PKG ?= src
TESTS ?= tests
SRC := $(PKG) $(TESTS)

# ==== Meta ====
.PHONY: help default init lint type format test coverage check env-check clean

default: help

help:
	@echo "Targets:"
	@echo "   init       Install project and dev dependencies with uv"
	@echo "   lint       Run Ruff checks"
	@echo "   type       Run mypy"
	@echo "   format     Apply Ruff formatting"
	@echo "   test       Run pytest when tests exist"
	@echo "   coverage   Run pytest with coverage when tests exist"
	@echo "   check      Run lint, type, and test"
	@echo "   env-check  Verify expected local project files exist"
	@echo "   clean      Remove caches and build artifacts"

# ==== Setup ====
init:
	uv sync --dev

# ==== Quality gates ====
lint:
	@echo "Running Ruff lint..."
	@ruff check $(PKG) $(TESTS)
	@echo "Running Ruff format check..."
	@ruff format --check $(PKG) $(TESTS)

type:
	@if find $(TESTS) -type f -name "*.py" | grep -q .; then \
		mypy $(PKG) $(TESTS); \
	else \
		mypy $(PKG); \
	fi

format:
	ruff format $(SRC)

test:
	@if find $(TESTS) -type f -name "*.py" | grep -q .; then \
		pytest -q; \
	else \
		echo "No tests found under $(TESTS); skipping pytest."; \
	fi

coverage:
	@if find $(TESTS) -type f -name "*.py" | grep -q .; then \
		pytest -q --cov=$(PKG) --cov=$(TESTS) --cov-report=term-missing --cov-report=xml; \
	else \
		echo "No tests found under $(TESTS); skipping coverage."; \
	fi

check: lint type test

env-check:
	$(PYTHON) -m src.scripts.check_env

# ==== Hygiene ====
clean:
	rm -rf .pytest_cache .mypy_cache .ruff_cache .coverage coverage.xml dist build \
		$(PKG)/*.egg-info .benchmarks
	find . -type d -name "__pycache__" -exec rm -rf {} +
