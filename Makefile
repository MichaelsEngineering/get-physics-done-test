# ==== Configuration ====
PYTHON ?= python3
PKG ?= src
TESTS ?= tests
SRC := $(PKG) $(TESTS)
SYNC_DELETE_REMOTE ?= 0
UV ?= uv
UV_CACHE_DIR ?= .uv-cache
RUN := UV_CACHE_DIR=$(UV_CACHE_DIR) $(UV) run

# ==== Meta ====
.PHONY: help default init lint type format test coverage check env-check resume-check clean sync gate smoke security-audit sbom

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
	@echo "   gate       Run repository policy and workflow hardening checks"
	@echo "   smoke      Run the installed CLI smoke test"
	@echo "   security-audit  Scan the repo for common secret and workflow issues"
	@echo "   sbom       Generate a CycloneDX SBOM under runs/security/"
	@echo "   env-check  Verify expected local project files exist"
	@echo "   resume-check  Diagnose interrupted overnight runs and print recovery steps"
	@echo "   clean      Remove caches and build artifacts"
	@echo "   sync       Rebase local main on origin/main and prune merged branches"

# ==== Setup ====
init:
	UV_CACHE_DIR=$(UV_CACHE_DIR) $(UV) sync --dev

# ==== Quality gates ====
lint:
	@echo "Running Ruff lint..."
	@$(RUN) ruff check $(PKG) $(TESTS)
	@echo "Running Ruff format check..."
	@$(RUN) ruff format --check $(PKG) $(TESTS)

type:
	@if find $(TESTS) -type f -name "*.py" | grep -q .; then \
		$(RUN) mypy $(PKG) $(TESTS); \
	else \
		$(RUN) mypy $(PKG); \
	fi

format:
	$(RUN) ruff format $(SRC)

test:
	@if find $(TESTS) -type f -name "*.py" | grep -q .; then \
		$(RUN) pytest -q; \
	else \
		echo "No tests found under $(TESTS); skipping pytest."; \
	fi

coverage:
	@if find $(TESTS) -type f -name "*.py" | grep -q .; then \
		$(RUN) pytest -q --cov=$(PKG) --cov=$(TESTS) --cov-report=term-missing --cov-report=xml; \
	else \
		echo "No tests found under $(TESTS); skipping coverage."; \
	fi

check: lint type test

gate:
	$(RUN) python -m src.scripts.security_tools gate

smoke:
	@output="$$( $(RUN) gpd-test architecture )"; \
	if ! printf "%s" "$$output" | grep -q "architecture summary"; then \
		echo "Unexpected CLI output: $$output"; \
		exit 1; \
	fi

security-audit:
	$(RUN) python -m src.scripts.security_tools audit

sbom:
	$(RUN) python -m src.scripts.security_tools sbom

env-check:
	$(RUN) python -m src.scripts.check_env

resume-check:
	$(RUN) python -m src.scripts.check_env recover

# ==== Hygiene ====
clean:
	rm -rf .pytest_cache .mypy_cache .ruff_cache .coverage coverage.xml dist build \
		$(PKG)/*.egg-info *.egg-info .benchmarks
	find . -type d -name "__pycache__" -exec rm -rf {} +

sync:
	@echo "Syncing local main with origin/main and cleaning merged branches..."
	git fetch origin
	git checkout main
	git rebase origin/main
	@git branch --merged main | grep -v "main" | xargs -r git branch -d
	@if [ "$(SYNC_DELETE_REMOTE)" = "1" ]; then \
		echo "Deleting merged remote branches on origin..."; \
		git branch -r --merged origin/main | grep -vE "origin/(main|HEAD)" | sed "s|origin/||" | xargs -r -n1 git push origin --delete; \
	else \
		echo "Skipping remote branch deletion (set SYNC_DELETE_REMOTE=1 to enable)"; \
	fi
	@git remote prune origin
