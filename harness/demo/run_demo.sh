#!/usr/bin/env bash
# POLARIS IEEE demo harness — one command from repo root (clone optional).
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "$REPO_ROOT"

OUT_DIR="$REPO_ROOT/harness/demo/output"
mkdir -p "$OUT_DIR"
STAMP="$(date -u +%Y%m%dT%H%M%SZ)"
LOG="$OUT_DIR/demo-${STAMP}.log"

{
  echo "=== POLARIS demo harness ==="
  echo "utc: $(date -u -Iseconds)"
  echo "repo: $REPO_ROOT"
  echo "git: $(git rev-parse --short HEAD 2>/dev/null || echo 'unknown')"
  echo

  echo "--- make test (pytest via Makefile) ---"
  make test
  echo

  echo "--- make sim-flood ---"
  make sim-flood
  echo

  echo "--- API smoke (TestClient, no port) ---"
  python3 harness/demo/run_demo.py
  echo

  echo "=== demo complete ==="
} 2>&1 | tee "$LOG"

echo "Wrote $LOG"
