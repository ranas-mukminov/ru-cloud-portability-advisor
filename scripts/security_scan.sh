#!/usr/bin/env bash
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd -P)"

missing() {
  echo "Required tool '$1' is not installed. Install via 'pip install .[dev]' or pip install $2." >&2
  exit 1
}

command -v pip-audit >/dev/null 2>&1 || missing "pip-audit" "pip-audit"
command -v bandit >/dev/null 2>&1 || missing "bandit" "bandit"

echo "[security] Running pip-audit against the current environment..."
pip-audit

echo "[security] Running bandit against src/ and examples/..."
bandit -q -r "$REPO_ROOT/src" "$REPO_ROOT/examples"

echo "[security] Completed security scan."
