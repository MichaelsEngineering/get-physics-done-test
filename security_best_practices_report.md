# Security Best Practices Report

## Executive Summary

No hardcoded credentials or obvious code-execution sinks showed up in the Python code during this review. The main issues are repository hygiene and CI supply-chain hardening: local research/session artifacts are currently one accidental `git add .` away from publication, several GitHub Actions are referenced by mutable tags instead of immutable SHAs, and some declared security jobs call missing Make targets, which leaves gaps in the repo's actual protections.

## Moderate Severity

### SBP-001: Local operational artifacts are not ignored and already contain workstation metadata

Impact: A routine bulk commit could publish local paths, session metadata, process metadata, and research trace logs to a public repository.

- [`.gitignore` lines 1-40](/home/qol/get-physics-done-test/.gitignore#L1) do not ignore `.gpd/`, `paper_runs/`, generated LaTeX artifacts, or other research-run outputs.
- [`.gpd/observability/current-session.json:5` ](/home/qol/get-physics-done-test/.gpd/observability/current-session.json#L5) contains the absolute local path `/home/qol/get-physics-done-test`.
- [`.gpd/observability/sessions/20260315T232504-2-a364e3.jsonl:1` ](/home/qol/get-physics-done-test/.gpd/observability/sessions/20260315T232504-2-a364e3.jsonl#L1) contains session IDs, timestamps, command metadata, and the same absolute path.
- [`run_config.yaml:1` ](/home/qol/get-physics-done-test/run_config.yaml#L1) and [`.git status --short` at review time] show active run metadata and untracked research directories present in the working tree.

Why it matters:
- This is a common personal-GitHub failure mode: local traces and generated work products are not secrets in the narrow sense, but they leak environment details and operational history.
- The risk is elevated because these directories are already present and untracked, so a broad staging command would include them unless the ignore rules are tightened.

Recommended fix:
- Add `.gpd/`, `paper_runs/`, `*.aux`, `*.log`, `*.out`, `*.pdf`, and any other generated research artifacts to `.gitignore` unless there is a deliberate reason to publish them.
- If some outputs must remain versioned, split publishable artifacts into a dedicated tracked directory and keep raw traces/session state ignored.

### SBP-002: Some GitHub Actions are pinned to mutable tags instead of immutable SHAs

Impact: If an upstream action tag is retargeted or the publisher is compromised, your CI or security workflow can execute attacker-controlled code.

- [`.github/workflows/codeql.yml:60` ](/home/qol/get-physics-done-test/.github/workflows/codeql.yml#L60) uses `actions/checkout@v4`.
- [`.github/workflows/codeql.yml:70` ](/home/qol/get-physics-done-test/.github/workflows/codeql.yml#L70) uses `github/codeql-action/init@v4`.
- [`.github/workflows/codeql.yml:99` ](/home/qol/get-physics-done-test/.github/workflows/codeql.yml#L99) uses `github/codeql-action/analyze@v4`.
- [`.github/workflows/security.yml:26` ](/home/qol/get-physics-done-test/.github/workflows/security.yml#L26) uses `github/codeql-action/init@v3`.
- [`.github/workflows/security.yml:30` ](/home/qol/get-physics-done-test/.github/workflows/security.yml#L30) uses `github/codeql-action/analyze@v3`.
- [`.github/workflows/security.yml:100` ](/home/qol/get-physics-done-test/.github/workflows/security.yml#L100) uses `actions/attest-build-provenance@v1`.

Why it matters:
- Personal repositories are frequently targeted through CI because workflows run automatically on pushes and pull requests.
- You already pin several actions by SHA elsewhere, so this inconsistency is avoidable.

Recommended fix:
- Pin all third-party actions to verified immutable commit SHAs, including CodeQL and attestation steps.
- Keep Dependabot enabled for GitHub Actions so SHA bumps remain manageable.

## Low Severity

### SBP-003: Security workflow claims do not currently map to real local commands

Impact: The repository advertises security jobs that currently fail immediately, reducing trust in the protections you think are running.

- [`.github/workflows/ci.yml:45` ](/home/qol/get-physics-done-test/.github/workflows/ci.yml#L45) calls `uv run make gate`.
- [`.github/workflows/ci.yml:62` ](/home/qol/get-physics-done-test/.github/workflows/ci.yml#L62) calls `uv run make smoke`.
- [`.github/workflows/security.yml:49` ](/home/qol/get-physics-done-test/.github/workflows/security.yml#L49) calls `uv run make security-audit`.
- [`.github/workflows/security.yml:68` ](/home/qol/get-physics-done-test/.github/workflows/security.yml#L68) and [`.github/workflows/security.yml:97` ](/home/qol/get-physics-done-test/.github/workflows/security.yml#L97) call `uv run make sbom`.
- [`Makefile:9` ](/home/qol/get-physics-done-test/Makefile#L9) defines the full `.PHONY` target set, and it does not include `gate`, `smoke`, `security-audit`, or `sbom`.
- Local verification during review: `make gate`, `make security-audit`, and `make sbom` each returned `No rule to make target`.

Why it matters:
- This is a security blind spot rather than a direct exploit.
- Broken checks mean dependency audit, SBOM generation, and higher-assurance validation are not actually available when the workflows run.

Recommended fix:
- Either implement those targets in [`Makefile`](/home/qol/get-physics-done-test/Makefile) or remove the jobs until they exist.
- Treat a green security pipeline as meaningful only after the commands can run locally and in CI.

## Informational

### INFO-001: No hardcoded credentials found in the scanned files

The review did not find obvious committed credentials, API tokens, SSH private keys, or AWS-style secrets in the current workspace using pattern-based scanning. That is good, but it should not replace a dedicated secret-scanning tool in CI.

## Suggested Next Steps

1. Tighten `.gitignore` to exclude `.gpd/`, `paper_runs/`, and generated document artifacts.
2. Pin all remaining GitHub Actions to immutable SHAs.
3. Implement or remove `gate`, `smoke`, `security-audit`, and `sbom` targets so the security workflows represent real controls.
