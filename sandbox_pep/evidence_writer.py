from __future__ import annotations

import csv
import json
from pathlib import Path
from typing import Any

from harness.reports.export_csv import export_csv
from harness.reports.summarize import summarize
from harness.utils.io import write_jsonl


def write_outputs(rows: list[dict[str, Any]], output_dir: Path, manifest: dict[str, Any]) -> dict[str, str]:
    output_dir.mkdir(parents=True, exist_ok=True)
    raw_jsonl = output_dir / "matrix_records.jsonl"
    normalized_csv = output_dir / "matrix_records.csv"
    timing_csv = output_dir / "timing_records.csv"
    summary_md = output_dir / "SUMMARY.md"
    manifest_path = output_dir / "run_manifest.json"
    write_jsonl(raw_jsonl, rows)
    export_csv(str(raw_jsonl), str(normalized_csv))
    _write_timing_csv(rows, timing_csv)
    summarize(str(raw_jsonl), str(summary_md))
    manifest_path.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return {
        "raw_jsonl": str(raw_jsonl),
        "normalized_csv": str(normalized_csv),
        "timing_csv": str(timing_csv),
        "summary_md": str(summary_md),
        "manifest_path": str(manifest_path),
    }


def _write_timing_csv(rows: list[dict[str, Any]], target: Path) -> None:
    fieldnames = [
        "condition",
        "task_id",
        "final_decision",
        "infrastructure_status",
        "infrastructure_reason",
        "latency_ms",
        "model_latency_ms",
        "parser_status",
        "tool_proposal_source",
        "is_model_generated_action",
        "fallback_used",
        "proposal_failure_reason",
        "model_backend_failure",
        "aegis_decision_attempted",
        "aegis_direct_decision_ms",
        "mesh_correlation_id",
        "mesh_request_id",
        "mesh_run_id",
        "decision_timeout_budget_ms",
        "decision_max_attempts",
        "decision_attempts_json",
        "aegis_timings_ms_json",
        "mock_tool_applied",
        "evidence_complete",
        "mesh_route_label",
        "trust_config_label",
        "escalation_pending",
        "escalation_id",
        "senate_tally_id",
        "senate_escalation_status",
        "receipt_status",
        "finality_status",
        "retry_after_ms",
    ]
    with target.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            hop_timings = row.get("hop_timings", {}) if isinstance(row.get("hop_timings"), dict) else {}
            writer.writerow(
                {
                    "condition": row.get("condition"),
                    "task_id": row.get("task_id"),
                    "final_decision": row.get("final_decision"),
                    "infrastructure_status": row.get("infrastructure_status"),
                    "infrastructure_reason": row.get("infrastructure_reason"),
                    "latency_ms": row.get("latency_ms"),
                    "model_latency_ms": row.get("model_latency_ms"),
                    "parser_status": row.get("parser_status"),
                    "tool_proposal_source": row.get("tool_proposal_source"),
                    "is_model_generated_action": row.get("is_model_generated_action"),
                    "fallback_used": row.get("fallback_used"),
                    "proposal_failure_reason": row.get("proposal_failure_reason"),
                    "model_backend_failure": row.get("model_backend_failure"),
                    "aegis_decision_attempted": row.get("aegis_decision_attempted"),
                    "aegis_direct_decision_ms": hop_timings.get("aegis_direct_decision_ms"),
                    "mesh_correlation_id": row.get("mesh_correlation_id") or hop_timings.get("mesh_correlation_id"),
                    "mesh_request_id": row.get("mesh_request_id") or hop_timings.get("mesh_request_id"),
                    "mesh_run_id": row.get("mesh_run_id") or hop_timings.get("mesh_run_id"),
                    "decision_timeout_budget_ms": row.get("decision_timeout_budget_ms")
                    or hop_timings.get("timeout_budget_ms"),
                    "decision_max_attempts": row.get("decision_max_attempts") or hop_timings.get("max_attempts"),
                    "decision_attempts_json": json.dumps(row.get("decision_attempts") or hop_timings.get("decision_attempts", []), sort_keys=True),
                    "aegis_timings_ms_json": json.dumps(hop_timings.get("aegis_timings_ms", {}), sort_keys=True),
                    "mock_tool_applied": row.get("mock_tool_applied"),
                    "evidence_complete": row.get("evidence_complete"),
                    "mesh_route_label": row.get("mesh_route_label"),
                    "trust_config_label": row.get("trust_config_label"),
                    "escalation_pending": row.get("escalation_pending"),
                    "escalation_id": row.get("escalation_id"),
                    "senate_tally_id": row.get("senate_tally_id"),
                    "senate_escalation_status": row.get("senate_escalation_status"),
                    "receipt_status": row.get("receipt_status"),
                    "finality_status": row.get("finality_status"),
                    "retry_after_ms": row.get("retry_after_ms"),
                }
            )
