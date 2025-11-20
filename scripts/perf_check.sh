#!/usr/bin/env bash
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd -P)"
RESOURCE_COUNT="${RESOURCE_COUNT:-200}"
TMP_DIR="$(mktemp -d)"
CONFIG_PATH="$REPO_ROOT/src/ru_cloud_portability_advisor/config/examples/aws_to_yc_simple.yaml"

if [[ ! -f "$CONFIG_PATH" ]]; then
  echo "Config file not found at $CONFIG_PATH" >&2
  exit 1
fi

command -v ru-cloud-advisor >/dev/null 2>&1 || {
  echo "CLI 'ru-cloud-advisor' not found. Install with 'pip install -e .[dev]' first." >&2
  exit 1
}

cleanup() {
  rm -rf "$TMP_DIR"
}
trap cleanup EXIT

cat >"$TMP_DIR/main.tf" <<'EOF'
terraform {
  required_version = ">= 1.3.0"
}

provider "aws" {
  region = "us-east-1"
}
EOF

for i in $(seq 1 "$RESOURCE_COUNT"); do
  cat >>"$TMP_DIR/main.tf" <<EOF
resource "aws_s3_bucket" "perf_bucket_${i}" {
  bucket = "perf-bucket-${i}"
}

resource "aws_sqs_queue" "perf_queue_${i}" {
  name = "perf-queue-${i}"
}
EOF
done

START_TS=$(date +%s)
ru-cloud-advisor analyze-project --tf-path "$TMP_DIR" --config "$CONFIG_PATH" --out "$TMP_DIR/report.json"
END_TS=$(date +%s)

echo "[perf] Synthetic Terraform generated at $TMP_DIR"
echo "[perf] Resources generated: $((RESOURCE_COUNT * 2))"
echo "[perf] Report location: $TMP_DIR/report.json (size: $(du -h "$TMP_DIR/report.json" | cut -f1))"
echo "[perf] Elapsed: $((END_TS - START_TS))s"
