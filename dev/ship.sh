#!/usr/bin/env bash
set -euo pipefail

# Usage: dev/ship.sh "feat: add parity experiment config"
MSG="${1:-}"

if [ -z "$MSG" ]; then
  echo "Usage: dev/ship.sh \"type: concise summary\""
  exit 1
fi

if ! git diff --quiet; then
  echo "Unstaged changes detected. Stage the exact files you want to ship first."
  exit 1
fi

if [ -n "$(git ls-files --others --exclude-standard)" ]; then
  echo "Untracked files detected. Add or ignore them before shipping."
  exit 1
fi

if git diff --cached --quiet; then
  echo "No staged changes to commit."
  exit 1
fi

# Create feature branch if on main
CUR_BRANCH=$(git rev-parse --abbrev-ref HEAD)
if [ "$CUR_BRANCH" = "main" ]; then
  NEW="feat/$(date +%y%m%d-%H%M%S)"
  echo "On main. Creating branch $NEW"
  git checkout -b "$NEW"
fi

echo "Running checks..."
make check

git commit -m "$MSG"

echo "Rebasing on latest origin/main..."
git fetch origin
git rebase origin/main

echo "Pushing..."
git push -u origin HEAD

REPO_PATH=$(git config --get remote.origin.url | sed -E 's#(git@|https://)github.com[:/]|\.git##g')
BRANCH=$(git rev-parse --abbrev-ref HEAD)
echo "Open a PR:"
echo "https://github.com/${REPO_PATH}/compare/main...${BRANCH}?expand=1"
