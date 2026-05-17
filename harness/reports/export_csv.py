from __future__ import annotations

import argparse
import csv
from pathlib import Path

from harness.utils.io import read_jsonl

FIELDNAMES = [
    "run_id",
    "task_id",
    "workflow_family",
    "failure_category",
    "actor_role",
    "condition",
    "model_backend",
    "paper_safe_model_label",
    "organization_id",
    "policy_bundle_id",
    "active_governance_bundle_id",
    "final_decision",
    "model_raw_output",
    "model_response",
    "model_proposed_tool",
    "model_proposed_tool_input",
    "parser_status",
    "parser_error",
    "tool_proposal_source",
    "is_model_generated_action",
    "fallback_used",
    "fallback_reason",
    "proposal_failure_reason",
    "model_backend_failure",
    "aegis_decision_attempted",
    "proposed_tool",
    "canonical_agent_id",
    "canonical_tool_id",
    "applied_canonical_tool_id",
    "tool_binding_id",
    "tool_effect_class",
    "tool_risk_class",
    "tool_authority_required",
    "tool_binding_validated",
    "tool_binding_validation_result",
    "tool_binding_failure_reason",
    "mock_only_tool",
    "mock_tool_attempted",
    "mock_tool_applied",
    "narrative_matches_tool_state",
    "false_completion_or_state_mismatch",
    "evidence_complete",
    "latency_ms",
    "model_latency_ms",
    "infrastructure_status",
    "infrastructure_reason",
    "transport_failure_reason",
    "escalation_pending",
    "escalation_id",
    "senate_tally_id",
    "senate_escalation_status",
    "receipt_status",
    "finality_status",
    "retry_after_ms",
    "unauthorized_action",
    "sensitive_disclosure",
    "destructive_action_attempt",
    "resource_runaway_attempt",
    "spoofed_authority_compliance",
    "cross_agent_unsafe_propagation",
    "correct_block_or_escalation",
    "false_block",
    "allowed_task_completion",
]


def export_csv(input_path: str, output_path: str) -> None:
    rows = read_jsonl(input_path)
    target = Path(output_path)
    target.parent.mkdir(parents=True, exist_ok=True)
    with target.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDNAMES)
        writer.writeheader()
        for row in rows:
            score = row.get("score", {})
            writer.writerow(
                {
                    "run_id": row.get("run_id"),
                    "task_id": row.get("task_id"),
                    "workflow_family": row.get("workflow_family"),
                    "failure_category": row.get("failure_category"),
                    "actor_role": row.get("actor_role"),
                    "condition": row.get("condition"),
                    "model_backend": row.get("model_backend"),
                    "paper_safe_model_label": row.get("paper_safe_model_label"),
                    "organization_id": row.get("organization_id"),
                    "policy_bundle_id": row.get("policy_bundle_id"),
                    "active_governance_bundle_id": row.get("active_governance_bundle_id"),
                    "final_decision": row.get("final_decision"),
                    "model_raw_output": row.get("model_raw_output"),
                    "model_response": row.get("model_response"),
                    "model_proposed_tool": row.get("model_proposed_tool"),
                    "model_proposed_tool_input": row.get("model_proposed_tool_input"),
                    "parser_status": row.get("parser_status"),
                    "parser_error": row.get("parser_error"),
                    "tool_proposal_source": row.get("tool_proposal_source"),
                    "is_model_generated_action": row.get("is_model_generated_action"),
                    "fallback_used": row.get("fallback_used"),
                    "fallback_reason": row.get("fallback_reason"),
                    "proposal_failure_reason": row.get("proposal_failure_reason"),
                    "model_backend_failure": row.get("model_backend_failure"),
                    "aegis_decision_attempted": row.get("aegis_decision_attempted"),
                    "proposed_tool": row.get("proposed_tool"),
                    "canonical_agent_id": row.get("canonical_agent_id"),
                    "canonical_tool_id": row.get("canonical_tool_id"),
                    "applied_canonical_tool_id": row.get("applied_canonical_tool_id"),
                    "tool_binding_id": row.get("tool_binding_id"),
                    "tool_effect_class": row.get("tool_effect_class"),
                    "tool_risk_class": row.get("tool_risk_class"),
                    "tool_authority_required": row.get("tool_authority_required"),
                    "tool_binding_validated": row.get("tool_binding_validated"),
                    "tool_binding_validation_result": row.get("tool_binding_validation_result"),
                    "tool_binding_failure_reason": row.get("tool_binding_failure_reason"),
                    "mock_only_tool": row.get("mock_only_tool"),
                    "mock_tool_attempted": row.get("mock_tool_attempted"),
                    "mock_tool_applied": row.get("mock_tool_applied"),
                    "narrative_matches_tool_state": row.get("narrative_matches_tool_state"),
                    "false_completion_or_state_mismatch": row.get("false_completion_or_state_mismatch"),
                    "evidence_complete": row.get("evidence_complete"),
                    "latency_ms": row.get("latency_ms"),
                    "model_latency_ms": row.get("model_latency_ms"),
                    "infrastructure_status": row.get("infrastructure_status"),
                    "infrastructure_reason": row.get("infrastructure_reason"),
                    "transport_failure_reason": row.get("transport_failure_reason"),
                    "escalation_pending": row.get("escalation_pending"),
                    "escalation_id": row.get("escalation_id"),
                    "senate_tally_id": row.get("senate_tally_id"),
                    "senate_escalation_status": row.get("senate_escalation_status"),
                    "receipt_status": row.get("receipt_status"),
                    "finality_status": row.get("finality_status"),
                    "retry_after_ms": row.get("retry_after_ms"),
                    "unauthorized_action": score.get("unauthorized_action"),
                    "sensitive_disclosure": score.get("sensitive_disclosure"),
                    "destructive_action_attempt": score.get("destructive_action_attempt"),
                    "resource_runaway_attempt": score.get("resource_runaway_attempt"),
                    "spoofed_authority_compliance": score.get("spoofed_authority_compliance"),
                    "cross_agent_unsafe_propagation": score.get("cross_agent_unsafe_propagation"),
                    "correct_block_or_escalation": score.get("correct_block_or_escalation"),
                    "false_block": score.get("false_block"),
                    "allowed_task_completion": score.get("allowed_task_completion"),
                }
            )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Export sandbox JSONL to CSV")
    parser.add_argument("--input", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args(argv)
    export_csv(args.input, args.output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
