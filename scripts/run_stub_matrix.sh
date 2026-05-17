#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

mkdir -p outputs/stub_matrix

declare -A AGENTS=(
  [plain_mesh_agent]=plain_employee_agent
  [prompt_policy_mesh_agent]=prompt_policy_employee_agent
  [aegis_governed_mesh_agent]=aegis_governed_employee_agent
)

for condition in plain_mesh_agent prompt_policy_mesh_agent aegis_governed_mesh_agent; do
  output="outputs/stub_matrix/${condition}.jsonl"
  python3 -m harness.runner     --task fixtures/tasks/smoke_tasks.yaml     --agents config/agents.example.yaml     --condition "$condition"     --agent-id "${AGENTS[$condition]}"     --model stub_model     --output "$output"

  python3 -m harness.reports.export_csv     --input "$output"     --output "outputs/stub_matrix/${condition}.csv"
done

python3 -m harness.reports.summarize   --input outputs/stub_matrix   --output outputs/stub_matrix/SUMMARY.md
