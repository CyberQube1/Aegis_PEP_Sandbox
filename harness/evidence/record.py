from __future__ import annotations

from typing import Any

REQUIRED_OUTPUT_FIELDS = (
    'run_id',
    'task_id',
    'condition',
    'model_backend',
    'model_version',
    'paper_safe_model_label',
    'model_adapter_status',
    'agent_id',
    'organization_id',
    'policy_bundle_id',
    'active_governance_bundle_id',
    'failure_category',
    'workflow_family',
    'actor_role',
    'expected_outcome',
    'model_narrative',
    'model_raw_output',
    'model_response',
    'model_proposed_tool',
    'model_proposed_tool_input',
    'proposed_action',
    'proposed_tool',
    'proposed_tool_input',
    'aegis_decision',
    'final_decision',
    'tool_call_attempted',
    'tool_call_applied',
    'mock_tool_attempted',
    'mock_tool_applied',
    'final_mock_state',
    'evidence_refs',
    'evidence_complete',
    'ilk_refs',
    'score',
    'latency_ms',
    'model_latency_ms',
    'tool_proposal_source',
    'is_model_generated_action',
    'fallback_used',
    'fallback_reason',
    'parser_status',
    'parser_error',
    'proposal_failure_reason',
    'parse_status',
    'parse_error',
    'narrative_matches_tool_state',
    'false_completion_or_state_mismatch',
    'infrastructure_status',
    'error_classification',
    'config_hash',
    'git_commit',
    'run_metadata',
)


def validate_record(record: dict[str, Any]) -> None:
    missing = [field for field in REQUIRED_OUTPUT_FIELDS if field not in record]
    if missing:
        raise ValueError(f'missing output fields: {missing}')
