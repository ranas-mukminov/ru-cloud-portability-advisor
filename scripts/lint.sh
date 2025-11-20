#!/usr/bin/env bash
set -euo pipefail

ruff src tests
black --check src tests
isort --check-only src tests
mypy src
yamllint src examples

