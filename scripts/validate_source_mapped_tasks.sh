#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

python3 - <<'PY'
from pathlib import Path
import sys
import yaml

root = Path('.')
control_files = [
    root / 'controls/internal_enterprise/controls.yaml',
    root / 'controls/apra_asic_au_finance/controls.yaml',
    root / 'controls/agentic_failure_taxonomy/controls.yaml',
]
task_files = [
    root / 'tasks/email_external_comms.yaml',
    root / 'tasks/vendor_service_provider.yaml',
    root / 'tasks/ai_consumer_impact.yaml',
    root / 'tasks/agentic_authority_tool_use.yaml',
    root / 'tasks/active_law_change.yaml',
]
required_task_fields = {
    'task_id', 'workflow_family', 'failure_category', 'jurisdiction_profile',
    'actor_role', 'prompt_text', 'available_context', 'expected_outcome',
    'prohibited_outcome', 'required_controls', 'source_mapping',
    'mock_tool_required', 'scoring_notes', 'evidence_expectations',
    'stub_behavior', 'policy_bundle_id', 'allowed_mock_tools',
    'source_mapping_level', 'source_refs', 'initial_mock_state',
}
required_control_fields = {
    'control_id', 'control_family', 'title', 'description', 'required_behavior',
    'prohibited_behavior', 'expected_outcomes', 'applicable_workflows',
    'source_mapping', 'claim_boundary',
}
allowed_mapping_levels = {
    'existing_praxis_source', 'baseline_pack_release', 'published_bundle_artifact',
    'indexed_graph_artifact', 'uploaded_internal_policy', 'curated_sandbox_copy',
    'synthetic_control', 'pending_praxis_org_association',
}

for path in [
    root / 'source_maps/missing_sources.yaml',
    root / 'source_maps/PRAXIS_SANDBOX_ORG_STATUS.md',
    root / 'source_maps/baseline_pack_sources.yaml',
]:
    if not path.exists() or path.stat().st_size == 0:
        raise SystemExit(f'missing required status/source file: {path}')

control_ids = set()
for path in control_files:
    data = yaml.safe_load(path.read_text(encoding='utf-8'))
    controls = data.get('controls', [])
    if not controls:
        raise SystemExit(f'no controls in {path}')
    for control in controls:
        missing = sorted(required_control_fields - set(control))
        if missing:
            raise SystemExit(f'{path}: control {control.get("control_id")} missing fields {missing}')
        control_ids.add(control['control_id'])

task_counts = {}
for path in task_files:
    data = yaml.safe_load(path.read_text(encoding='utf-8'))
    tasks = data.get('tasks', [])
    if not tasks:
        raise SystemExit(f'no tasks in {path}')
    task_counts[path.name] = len(tasks)
    for task in tasks:
        missing = sorted(required_task_fields - set(task))
        if missing:
            raise SystemExit(f'{path}: task {task.get("task_id")} missing fields {missing}')
        missing_controls = [cid for cid in task['required_controls'] if cid not in control_ids]
        if missing_controls:
            raise SystemExit(f'{path}: task {task["task_id"]} references unknown controls {missing_controls}')
        if task['source_mapping_level'] not in allowed_mapping_levels:
            raise SystemExit(f'{path}: task {task["task_id"]} has invalid source_mapping_level {task["source_mapping_level"]}')
        if not task['source_mapping']:
            raise SystemExit(f'{path}: task {task["task_id"]} has empty source_mapping')
        if not task['source_refs']:
            raise SystemExit(f'{path}: task {task["task_id"]} has empty source_refs')

expected_counts = {
    'email_external_comms.yaml': 8,
    'vendor_service_provider.yaml': 8,
    'ai_consumer_impact.yaml': 8,
    'agentic_authority_tool_use.yaml': 12,
    'active_law_change.yaml': 6,
}
for name, expected in expected_counts.items():
    actual = task_counts.get(name)
    if actual != expected:
        raise SystemExit(f'{name}: expected {expected} tasks, found {actual}')

print('schema validation ok')
PY

mkdir -p outputs/prompt_c_validation

for spec in \
  "plain_mesh_agent plain_employee_agent" \
  "prompt_policy_mesh_agent prompt_policy_employee_agent" \
  "aegis_governed_mesh_agent aegis_governed_employee_agent"
do
  set -- $spec
  condition="$1"
  agent_id="$2"
  for task_file in \
    tasks/email_external_comms.yaml \
    tasks/vendor_service_provider.yaml \
    tasks/ai_consumer_impact.yaml \
    tasks/agentic_authority_tool_use.yaml \
    tasks/active_law_change.yaml
  do
    name="$(basename "$task_file" .yaml)"
    python3 -m harness.runner \
      --task "$task_file" \
      --agents config/agents.example.yaml \
      --condition "$condition" \
      --model stub_model \
      --agent-id "$agent_id" \
      --output "outputs/prompt_c_validation/${condition}_${name}.jsonl"
  done
done

echo "validate_source_mapped_tasks.sh: ok"
