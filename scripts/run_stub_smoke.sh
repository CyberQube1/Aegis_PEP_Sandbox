#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

mkdir -p outputs/stub_smoke

python3 -m harness.runner   --task fixtures/tasks/smoke_tasks.yaml   --agents config/agents.example.yaml   --condition plain_mesh_agent   --model stub_model   --output outputs/stub_smoke/plain.jsonl

python3 -m harness.reports.export_csv   --input outputs/stub_smoke/plain.jsonl   --output outputs/stub_smoke/plain.csv

python3 -m harness.reports.summarize   --input outputs/stub_smoke/plain.jsonl   --output outputs/stub_smoke/SUMMARY.md
