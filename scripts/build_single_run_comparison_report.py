#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import json
import shutil
from collections import Counter
from pathlib import Path
from statistics import mean
from typing import Any, Callable


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_PACK_DIR = ROOT / "reports" / "One Run Folder" / "One Run Comparison"
DETAIL_DIR_NAME = "single_run_report"
TOP_REPORT_NAME = "SINGLE_RUN_COMPARISON_REPORT.md"
EXPECTED_TOTAL_ROWS = 126
EXPECTED_GOVERNED_ROWS = 42
EXPECTED_CONDITIONS = {"plain_mesh_agent", "prompt_policy_mesh_agent", "aegis_governed_mesh_agent"}

RUN_PACKS = [
    {
        "run_label": "stubbed_1x",
        "display": "Stubbed 1x",
        "paper_model_label": "stub_model",
        "temperature": "N/A",
        "pack_label": "Stubbed one run",
        "pack": ROOT / "reports" / "One Run Folder" / "Stubbed one run",
        "raw": "stubbed_output",
        "report": "stubbed_report",
    },
    {
        "run_label": "gemma_1x",
        "display": "Gemma 1x",
        "paper_model_label": "gemma_local",
        "temperature": "0",
        "pack_label": "Gemma one run",
        "pack": ROOT / "reports" / "One Run Folder" / "Gemma one run",
        "raw": "gemma_output",
        "report": "gemma_report",
    },
    {
        "run_label": "frontier_temp0_1x",
        "display": "Frontier temp 0 1x",
        "paper_model_label": "frontier_model_a",
        "temperature": "0",
        "pack_label": "Frontier temp 0 one run",
        "pack": ROOT / "reports" / "One Run Folder" / "Frontier temp 0 one run",
        "raw": "frontier_output",
        "report": "frontier_report",
    },
    {
        "run_label": "frontier_temp07_1x",
        "display": "Frontier temp 0.7 1x",
        "paper_model_label": "frontier_model_a",
        "temperature": "0.7",
        "pack_label": "Frontier temp 0.7 one run",
        "pack": ROOT / "reports" / "One Run Folder" / "Frontier temp 0.7 one run",
        "raw": "frontier_output",
        "report": "frontier_report",
    },
    {
        "run_label": "frontier_temp10_1x",
        "display": "Frontier temp 1.0 1x",
        "paper_model_label": "frontier_model_a",
        "temperature": "1.0",
        "pack_label": "Frontier temp 1.0 one run",
        "pack": ROOT / "reports" / "One Run Folder" / "Frontier temp 1.0 one run",
        "raw": "frontier_output",
        "report": "frontier_report",
    },
]

RAW_REQUIRED_FILES = [
    "matrix_records.jsonl",
    "matrix_records.csv",
    "run_manifest.json",
    "SUMMARY.md",
    "timing_records.csv",
]

REPORT_REQUIRED_FILES = [
    "AEGIS_GOVERNED_DECISION_HEADLINE.md",
    "AEGIS_GOVERNED_DECISION_HEADLINE.csv",
    "AEGIS_GOVERNED_DECISION_HEADLINE.json",
    "AEGIS_GOVERNED_DECISION_TRACE.csv",
    "AEGIS_GOVERNED_DECISION_TRACE.md",
    "AEGIS_GOVERNED_DECISION_TRACE.jsonl",
    "AEGIS_ARTIFACT_AUDIT.md",
    "AEGIS_ARTIFACT_AUDIT.json",
    "AEGIS_PROVENANCE_BOUNDARY_AUDIT.md",
    "AEGIS_PROVENANCE_BOUNDARY_AUDIT.json",
    "AEGIS_RERUN_READINESS_SUMMARY.md",
    "REPORT_INDEX.md",
]

SENATE_REPORT_FILES = [
    "AEGIS_SENATE_ASYNC_STATUS_SUMMARY.md",
    "AEGIS_SENATE_ASYNC_STATUS_TRACE.md",
    "AEGIS_SENATE_ASYNC_STATUS_TRACE.csv",
    "AEGIS_SENATE_BY_SETTLED_DECISION.md",
    "AEGIS_SENATE_SETTLED_ALLOWED_ACTIONS.md",
    "AEGIS_SENATE_SETTLED_DENIED_ACTIONS.md",
]

COPY_REPORTS = {
    "AEGIS_GOVERNED_DECISION_HEADLINE.md": "AEGIS_SINGLE_RUN_HEADLINE.md",
    "AEGIS_GOVERNED_DECISION_HEADLINE.csv": "AEGIS_SINGLE_RUN_HEADLINE.csv",
    "AEGIS_GOVERNED_DECISION_HEADLINE.json": "AEGIS_SINGLE_RUN_HEADLINE.json",
    "AEGIS_DECISION_BY_RUN_AND_BUCKET.md": "AEGIS_SINGLE_RUN_BY_DECISION_BUCKET.md",
    "AEGIS_DECISION_BY_EXPECTED_OUTCOME.md": "AEGIS_SINGLE_RUN_BY_EXPECTED_OUTCOME.md",
    "AEGIS_EXPECTED_VS_ACTUAL_DECISION_MATCH.md": "AEGIS_SINGLE_RUN_EXPECTED_VS_ACTUAL.md",
    "AEGIS_PRACTICAL_EXECUTION_OUTCOMES.md": "AEGIS_SINGLE_RUN_PRACTICAL_EXECUTION_OUTCOMES.md",
    "AEGIS_SENATE_BY_SETTLED_DECISION.md": "AEGIS_SINGLE_RUN_SENATE_BY_SETTLED_DECISION.md",
    "AEGIS_SENATE_SETTLED_ALLOWED_ACTIONS.md": "AEGIS_SINGLE_RUN_SENATE_SETTLED_ALLOWED_ACTIONS.md",
    "AEGIS_SENATE_SETTLED_DENIED_ACTIONS.md": "AEGIS_SINGLE_RUN_SENATE_SETTLED_DENIED_ACTIONS.md",
    "AEGIS_PROVENANCE_BOUNDARY_AUDIT.md": "AEGIS_SINGLE_RUN_PROVENANCE_BOUNDARY_AUDIT.md",
    "AEGIS_DECISION_BY_TOOL_AND_BUCKET.md": "AEGIS_SINGLE_RUN_BY_TOOL_AND_BUCKET.md",
    "AEGIS_DECISION_BY_CONTROL_AND_BUCKET.md": "AEGIS_SINGLE_RUN_BY_CONTROL_AND_BUCKET.md",
    "AEGIS_BLOCKED_ACTIONS.md": "AEGIS_SINGLE_RUN_BLOCKED_ACTIONS.md",
    "AEGIS_EXECUTION_WITHHELD_ACTIONS.md": "AEGIS_SINGLE_RUN_EXECUTION_WITHHELD_ACTIONS.md",
    "AEGIS_FAIL_CLOSED_NO_ACTIONS.md": "AEGIS_SINGLE_RUN_FAIL_CLOSED_NO_ACTIONS.md",
    "AEGIS_ALLOWED_OR_APPROVED_ACTIONS.md": "AEGIS_SINGLE_RUN_ALLOWED_OR_APPROVED_ACTIONS.md",
    "AEGIS_OTHER_OR_UNKNOWN_DECISIONS.md": "AEGIS_SINGLE_RUN_OTHER_OR_UNKNOWN_DECISIONS.md",
    "PROMPT_POLICY_LEAKAGE_WITH_AEGIS_COUNTERFACTUAL.md": "PROMPT_POLICY_LEAKAGE_WITH_AEGIS_COUNTERFACTUAL.md",
    "PROMPT_POLICY_LEAKAGE_WITH_AEGIS_COUNTERFACTUAL.csv": "PROMPT_POLICY_LEAKAGE_WITH_AEGIS_COUNTERFACTUAL.csv",
    "PROMPT_POLICY_LEAKAGE_WITH_AEGIS_COUNTERFACTUAL.jsonl": "PROMPT_POLICY_LEAKAGE_WITH_AEGIS_COUNTERFACTUAL.jsonl",
    "PROMPT_POLICY_LEAKAGE_EVENT_CHAIN.md": "PROMPT_POLICY_LEAKAGE_EVENT_CHAIN.md",
    "PROMPT_POLICY_LEAKAGE_EVENT_CHAIN.csv": "PROMPT_POLICY_LEAKAGE_EVENT_CHAIN.csv",
    "PROMPT_POLICY_LEAKAGE_EVENT_CHAIN.jsonl": "PROMPT_POLICY_LEAKAGE_EVENT_CHAIN.jsonl",
}

TRACE_COLUMNS = [
    "run_label",
    "paper_model_label",
    "temperature",
    "single_run_pack_label",
    "task_id",
    "task_title",
    "workflow_family",
    "failure_category",
    "expected_outcome",
    "condition",
    "model_proposal_action_type",
    "proposed_mock_tool",
    "proposed_recipient_target_resource",
    "proposed_payload_summary",
    "parser_status",
    "raw_aegis_decision",
    "aegis_decision",
    "normalized_decision_bucket",
    "practical_execution_outcome",
    "aegis_reason",
    "aegis_reason_codes",
    "aegis_policy_control_rule_ids",
    "required_controls",
    "source_refs",
    "source_mapping_level",
    "aegis_decision_attempted",
    "failed_closed_before_aegis_no_tool",
    "mock_tool_applied",
    "evidence_complete",
    "expected_vs_actual_decision_match",
    "governed_risky_side_effect_completed",
    "provenance_boundary_valid",
    "provenance_resolution_source",
    "provenance_status",
    "aegis_resolved_citations_present",
    "verified_active_law_source_refs_present",
    "evidence_record_path",
    "manifest_reference",
    "decision_id",
    "trace_id",
    "bundle_fingerprint",
    "deterministic_decision_hash",
    "senate_queued",
    "senate_tally_id",
    "senate_quorum_met",
    "senate_effective_finality",
    "senate_settled_decision",
    "senate_settled_latency_ms",
    "senate_snapshot_joined",
]


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Build the paper-facing single-run comparison pack from existing artifacts")
    parser.add_argument("--pack-dir", default=str(DEFAULT_PACK_DIR), help="Output pack directory containing comparison_report")
    args = parser.parse_args(argv)

    pack_dir = Path(args.pack_dir)
    source_report = pack_dir / "comparison_report"
    out_dir = pack_dir / DETAIL_DIR_NAME
    top_report = pack_dir / TOP_REPORT_NAME
    if not source_report.exists():
        raise SystemExit(f"Missing source comparison report: {source_report}")

    if out_dir.exists():
        shutil.rmtree(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    normalized_rows = read_csv(source_report / "normalized_results.csv")
    source_trace_rows = read_csv(source_report / "AEGIS_GOVERNED_DECISION_TRACE.csv")
    source_headline_rows = read_csv(source_report / "AEGIS_GOVERNED_DECISION_HEADLINE.csv")
    senate_summary_rows = read_csv(source_report / "AEGIS_SENATE_ASYNC_STATUS_SUMMARY.csv")
    leakage_rows = read_csv(source_report / "PROMPT_POLICY_LEAKAGE_WITH_AEGIS_COUNTERFACTUAL.csv")

    trace_rows = transform_governed_trace(source_trace_rows)
    write_csv(out_dir / "AEGIS_SINGLE_RUN_GOVERNED_DECISION_TRACE.csv", trace_rows, TRACE_COLUMNS)
    write_jsonl(out_dir / "AEGIS_SINGLE_RUN_GOVERNED_DECISION_TRACE.jsonl", trace_rows)
    write_md(out_dir / "AEGIS_SINGLE_RUN_GOVERNED_DECISION_TRACE.md", "# Aegis Single Run Governed Decision Trace\n\n" + markdown_table(trace_rows, TRACE_COLUMNS))

    for src_name, dest_name in COPY_REPORTS.items():
        src = source_report / src_name
        if src.exists():
            shutil.copy2(src, out_dir / dest_name)

    completeness = build_completeness(normalized_rows, trace_rows)
    headline = build_headline(normalized_rows, trace_rows, source_headline_rows, senate_summary_rows, completeness)
    aggregates = build_aggregates(headline, leakage_rows)

    write_csv(out_dir / "AEGIS_SINGLE_RUN_HEADLINE.csv", headline)
    write_json(out_dir / "AEGIS_SINGLE_RUN_HEADLINE.json", headline)
    write_md(out_dir / "AEGIS_SINGLE_RUN_HEADLINE.md", "# Aegis Single Run Headline\n\n" + markdown_table(headline))
    write_json(out_dir / "AEGIS_SINGLE_RUN_PACK_COMPLETENESS.json", completeness)
    write_md(out_dir / "AEGIS_SINGLE_RUN_PACK_COMPLETENESS.md", completeness_markdown(completeness))

    write_md(out_dir / "AEGIS_SINGLE_RUN_BY_MODEL.md", grouped_markdown("Aegis Single Run By Model", trace_rows, ["paper_model_label", "normalized_decision_bucket"]))
    write_md(out_dir / "AEGIS_SINGLE_RUN_BY_TEMPERATURE.md", grouped_markdown("Aegis Single Run By Temperature", trace_rows, ["temperature", "normalized_decision_bucket"]))
    write_md(out_dir / "AEGIS_SINGLE_RUN_BY_WORKFLOW_AND_BUCKET.md", grouped_markdown("Aegis Single Run By Workflow And Bucket", trace_rows, ["run_label", "workflow_family", "normalized_decision_bucket"]))
    write_md(out_dir / "AEGIS_SINGLE_RUN_BY_FAILURE_CATEGORY.md", grouped_markdown("Aegis Single Run By Failure Category", trace_rows, ["run_label", "failure_category", "normalized_decision_bucket"]))
    write_md(out_dir / "AEGIS_SINGLE_RUN_BY_TASK.md", grouped_markdown("Aegis Single Run By Task", trace_rows, ["task_id", "task_title", "run_label", "normalized_decision_bucket"]))
    write_md(out_dir / "AEGIS_SINGLE_RUN_BY_CONTROL_AND_BUCKET.md", exploded_grouped_markdown("Aegis Single Run By Control And Bucket", trace_rows, "required_controls", ["run_label", "normalized_decision_bucket"]))

    write_senate_files(out_dir, trace_rows, headline)
    write_md(out_dir / "AEGIS_SINGLE_RUN_PROVENANCE_SUMMARY.md", provenance_markdown(headline))
    write_md(out_dir / "AEGIS_SINGLE_RUN_PROVENANCE_BY_RUN.md", provenance_by_run_markdown(headline))
    write_md(out_dir / "AEGIS_SINGLE_RUN_RISK_OUTCOME_SUMMARY.md", risk_markdown(headline, leakage_rows))
    write_md(out_dir / "AEGIS_SINGLE_RUN_RISKY_COMPLETIONS.md", zero_or_table(
        "Aegis Single Run Risky Completions",
        trace_rows,
        lambda row: is_true(row.get("governed_risky_side_effect_completed")),
        ["run_label", "task_id", "task_title", "proposed_mock_tool", "aegis_decision", "practical_execution_outcome"],
        "Zero governed risky side-effect completions were found across the five single runs.",
    ))
    write_md(out_dir / "AEGIS_SINGLE_RUN_MOCK_TOOL_APPLICATIONS.md", zero_or_table(
        "Aegis Single Run Mock Tool Applications",
        trace_rows,
        lambda row: is_true(row.get("mock_tool_applied")),
        ["run_label", "task_id", "task_title", "proposed_mock_tool", "aegis_decision", "practical_execution_outcome"],
        "Zero governed mock tool applications were found across the five single runs.",
    ))
    write_action_tables(out_dir, trace_rows)
    write_md(out_dir / "AEGIS_SINGLE_RUN_RERUN_READINESS_SUMMARY.md", rerun_markdown(headline, completeness))
    write_md(out_dir / "AEGIS_SINGLE_RUN_PAPER_READINESS.md", paper_readiness_markdown(headline, completeness, aggregates))
    write_index(out_dir)
    write_top_report(top_report, headline, completeness, aggregates)

    print(json.dumps({
        "output_dir": str(pack_dir),
        "top_report": str(top_report),
        "detail_report_dir": str(out_dir),
        "total_rows": aggregates["total_rows"],
        "governed_rows": aggregates["governed_rows"],
        "pack_complete": aggregates["overall_pack_complete"],
        "paper_ready": aggregates["overall_paper_ready"],
    }, indent=2, sort_keys=True))
    return 0


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, Any]], columns: list[str] | None = None) -> None:
    columns = columns or (list(rows[0].keys()) if rows else [])
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=columns, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def write_json(path: Path, payload: Any) -> None:
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    path.write_text("".join(json.dumps(row, sort_keys=True) + "\n" for row in rows), encoding="utf-8")


def write_md(path: Path, text: str) -> None:
    path.write_text(text.rstrip() + "\n", encoding="utf-8")


def is_true(value: Any) -> bool:
    return str(value).strip().lower() in {"true", "1", "yes", "y"}


def as_int(value: Any) -> int:
    try:
        return int(float(str(value or "0")))
    except ValueError:
        return 0


def as_float(value: Any) -> float | None:
    try:
        return float(str(value))
    except (TypeError, ValueError):
        return None


def run_spec_by_label() -> dict[str, dict[str, Any]]:
    return {spec["run_label"]: spec for spec in RUN_PACKS}


def transform_governed_trace(rows: list[dict[str, str]]) -> list[dict[str, Any]]:
    specs = run_spec_by_label()
    transformed: list[dict[str, Any]] = []
    for row in rows:
        spec = specs.get(row.get("run_label", ""), {})
        senate_queued = bool(row.get("senate_escalation_id") or row.get("senate_tally_id") or row.get("senate_settled_decision"))
        out = {column: "N/A" for column in TRACE_COLUMNS}
        for column in TRACE_COLUMNS:
            if column in row and row.get(column) not in {None, ""}:
                out[column] = row[column]
        out["single_run_pack_label"] = spec.get("pack_label", out.get("run_label", "N/A"))
        out["temperature"] = row.get("temperature") or spec.get("temperature", "N/A")
        out["senate_queued"] = str(senate_queued).lower()
        out["senate_effective_finality"] = row.get("senate_effective_finality_status") or "N/A"
        out["senate_settled_latency_ms"] = row.get("senate_settlement_latency_ms") or "N/A"
        out["senate_snapshot_joined"] = row.get("senate_status_snapshot_available") or "false"
        out["senate_settled_decision"] = row.get("senate_settled_decision") or "N/A"
        transformed.append(out)
    return transformed


def build_completeness(normalized_rows: list[dict[str, str]], trace_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    by_run_total = Counter(row.get("run_label", "") for row in normalized_rows)
    by_run_governed = Counter(row.get("run_label", "") for row in trace_rows)
    conditions_by_run: dict[str, set[str]] = {}
    senate_by_run = Counter(row.get("run_label", "") for row in trace_rows if is_true(row.get("senate_queued")))
    records: list[dict[str, Any]] = []
    for row in normalized_rows:
        conditions_by_run.setdefault(row.get("run_label", ""), set()).add(row.get("condition", ""))

    for spec in RUN_PACKS:
        run = spec["run_label"]
        pack = Path(spec["pack"])
        raw_dir = pack / spec["raw"]
        report_dir = pack / spec["report"]
        missing_files: list[str] = []
        missing_fields: list[str] = []
        notes: list[str] = []
        if not raw_dir.exists():
            missing_files.append(rel(raw_dir))
        if not report_dir.exists():
            missing_files.append(rel(report_dir))
        for file_name in RAW_REQUIRED_FILES:
            if not (raw_dir / file_name).exists():
                missing_files.append(rel(raw_dir / file_name))
        for file_name in REPORT_REQUIRED_FILES:
            if not (report_dir / file_name).exists():
                missing_files.append(rel(report_dir / file_name))
        if senate_by_run[run] > 0:
            for file_name in SENATE_REPORT_FILES:
                if not (report_dir / file_name).exists():
                    missing_files.append(rel(report_dir / file_name))
        else:
            notes.append("Senate files are not required because no Senate queued rows were detected for this run.")

        actual_total = by_run_total[run]
        actual_governed = by_run_governed[run]
        observed_conditions = conditions_by_run.get(run, set())
        if actual_total != EXPECTED_TOTAL_ROWS:
            missing_fields.append(f"expected_total_rows={EXPECTED_TOTAL_ROWS}, actual_total_rows={actual_total}")
        if actual_governed != EXPECTED_GOVERNED_ROWS:
            missing_fields.append(f"expected_governed_rows={EXPECTED_GOVERNED_ROWS}, actual_governed_rows={actual_governed}")
        if observed_conditions != EXPECTED_CONDITIONS:
            missing_fields.append(f"expected_conditions={sorted(EXPECTED_CONDITIONS)}, observed_conditions={sorted(observed_conditions)}")
        if not missing_files and not missing_fields:
            notes.append("Complete single-run pack with expected 126 total rows, 42 governed rows, and all three conditions.")

        records.append({
            "run_label": run,
            "expected_total_rows": EXPECTED_TOTAL_ROWS,
            "actual_total_rows": actual_total,
            "expected_governed_rows": EXPECTED_GOVERNED_ROWS,
            "actual_governed_rows": actual_governed,
            "raw_output_present": raw_dir.exists(),
            "report_output_present": report_dir.exists(),
            "headline_present": (report_dir / "AEGIS_GOVERNED_DECISION_HEADLINE.md").exists(),
            "governed_trace_present": (report_dir / "AEGIS_GOVERNED_DECISION_TRACE.csv").exists(),
            "artifact_audit_present": (report_dir / "AEGIS_ARTIFACT_AUDIT.json").exists(),
            "provenance_audit_present": (report_dir / "AEGIS_PROVENANCE_BOUNDARY_AUDIT.json").exists(),
            "rerun_summary_present": (report_dir / "AEGIS_RERUN_READINESS_SUMMARY.md").exists(),
            "senate_summary_present": (report_dir / "AEGIS_SENATE_ASYNC_STATUS_SUMMARY.md").exists(),
            "senate_trace_present": (report_dir / "AEGIS_SENATE_ASYNC_STATUS_TRACE.csv").exists(),
            "matrix_records_present": (raw_dir / "matrix_records.jsonl").exists(),
            "run_manifest_present": (raw_dir / "run_manifest.json").exists(),
            "pack_complete": not missing_files and not missing_fields,
            "missing_files": missing_files,
            "missing_fields": missing_fields,
            "notes": " ".join(notes),
        })
    return records


def build_headline(
    normalized_rows: list[dict[str, str]],
    trace_rows: list[dict[str, Any]],
    source_headline_rows: list[dict[str, str]],
    senate_summary_rows: list[dict[str, str]],
    completeness: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    headline_by_run = {row.get("run_label", ""): row for row in source_headline_rows}
    senate_by_run = {row.get("run_label", ""): row for row in senate_summary_rows}
    complete_by_run = {row["run_label"]: row for row in completeness}
    rows: list[dict[str, Any]] = []
    for spec in RUN_PACKS:
        run = spec["run_label"]
        h = headline_by_run.get(run, {})
        s = senate_by_run.get(run, {})
        run_trace = [row for row in trace_rows if row.get("run_label") == run]
        total_rows = sum(1 for row in normalized_rows if row.get("run_label") == run)
        valid = as_int(h.get("provenance_boundary_valid_rows"))
        evidence = as_int(h.get("evidence_complete_rows"))
        governed = as_int(h.get("governed_rows"))
        completeness_row = complete_by_run.get(run, {})
        rows.append({
            "run_label": run,
            "paper_model_label": spec["paper_model_label"],
            "temperature": spec["temperature"],
            "source_pack": rel(Path(spec["pack"])),
            "total_rows": total_rows,
            "governed_rows": governed,
            "aegis_attempted_rows": as_int(h.get("aegis_attempted_rows")),
            "local_fail_closed_no_tool_rows": as_int(h.get("fail_closed_no_action_rows")),
            "initial_allow_or_approve_rows": as_int(h.get("allow_or_approve_rows")),
            "initial_block_rows": as_int(h.get("block_rows")),
            "initial_senate_escalation_rows": as_int(h.get("senate_escalation_rows")),
            "initial_execution_withheld_rows": as_int(h.get("execution_withheld_rows")),
            "parser_or_backend_failure_rows": as_int(h.get("parser_or_backend_failure_rows")),
            "other_rows": as_int(h.get("other_rows")),
            "senate_queued_rows": as_int(s.get("senate_rows")) or sum(1 for row in run_trace if is_true(row.get("senate_queued"))),
            "senate_snapshots_joined": as_int(s.get("snapshot_rows")) or sum(1 for row in run_trace if is_true(row.get("senate_snapshot_joined"))),
            "senate_settled_allowed_rows": as_int(s.get("settled_allowed_rows")),
            "senate_settled_denied_rows": as_int(s.get("settled_denied_rows")),
            "senate_settled_unknown_rows": as_int(s.get("settled_unknown_rows")),
            "senate_tally_present_rows": as_int(s.get("tally_present_rows")),
            "senate_quorum_met_rows": as_int(s.get("quorum_met_rows")),
            "senate_effective_finality_final_rows": as_int(s.get("effective_final_rows")),
            "mock_tool_applied_rows": as_int(h.get("mock_tool_applied_rows")),
            "governed_risky_side_effect_completions": as_int(h.get("governed_risky_side_effect_completions")),
            "evidence_complete_rows": evidence,
            "evidence_completeness_rate": h.get("evidence_completeness_rate", "N/A"),
            "trusted_aegis_resolved_provenance_rows": valid,
            "provenance_unknown_rows": as_int(h.get("provenance_boundary_unknown_rows")),
            "provenance_invalid_rows": as_int(h.get("provenance_boundary_invalid_rows")),
            "rerun_needed_for_risk_outcome_claims": h.get("rerun_needed_for_risk_outcome_claims", "unknown"),
            "rerun_needed_for_provenance_claims": h.get("rerun_needed_for_provenance_claims", "unknown"),
            "rerun_needed_for_full_paper_claims": h.get("rerun_needed_for_full_paper_claims", "unknown"),
            "rerun_recommended": h.get("rerun_recommended", "unknown"),
            "rerun_reason_short": h.get("rerun_reason_short", "N/A"),
            "pack_complete": completeness_row.get("pack_complete", False),
            "pack_completeness_notes": completeness_row.get("notes", "N/A"),
        })
    return rows


def build_aggregates(headline: list[dict[str, Any]], leakage_rows: list[dict[str, str]]) -> dict[str, Any]:
    totals = {
        "total_rows": sum(as_int(row.get("total_rows")) for row in headline),
        "governed_rows": sum(as_int(row.get("governed_rows")) for row in headline),
        "aegis_attempted_rows": sum(as_int(row.get("aegis_attempted_rows")) for row in headline),
        "local_fail_closed_no_tool_rows": sum(as_int(row.get("local_fail_closed_no_tool_rows")) for row in headline),
        "initial_execution_withheld_rows": sum(as_int(row.get("initial_execution_withheld_rows")) for row in headline),
        "senate_queued_rows": sum(as_int(row.get("senate_queued_rows")) for row in headline),
        "senate_settled_allowed_rows": sum(as_int(row.get("senate_settled_allowed_rows")) for row in headline),
        "senate_settled_denied_rows": sum(as_int(row.get("senate_settled_denied_rows")) for row in headline),
        "senate_tally_present_rows": sum(as_int(row.get("senate_tally_present_rows")) for row in headline),
        "senate_quorum_met_rows": sum(as_int(row.get("senate_quorum_met_rows")) for row in headline),
        "mock_tool_applied_rows": sum(as_int(row.get("mock_tool_applied_rows")) for row in headline),
        "governed_risky_side_effect_completions": sum(as_int(row.get("governed_risky_side_effect_completions")) for row in headline),
        "trusted_aegis_resolved_provenance_rows": sum(as_int(row.get("trusted_aegis_resolved_provenance_rows")) for row in headline),
        "provenance_unknown_rows": sum(as_int(row.get("provenance_unknown_rows")) for row in headline),
        "provenance_invalid_rows": sum(as_int(row.get("provenance_invalid_rows")) for row in headline),
        "prompt_policy_leakage_rows": len(leakage_rows),
    }
    totals["overall_pack_complete"] = all(is_true(row.get("pack_complete")) for row in headline)
    totals["overall_paper_ready"] = (
        totals["overall_pack_complete"]
        and totals["governed_risky_side_effect_completions"] == 0
        and totals["provenance_unknown_rows"] == 0
        and totals["provenance_invalid_rows"] == 0
        and all(str(row.get("rerun_recommended", "")).strip().lower() in {"no", "false", "n/a", "", "no_rerun_needed"} for row in headline)
    )
    return totals


def markdown_table(rows: list[dict[str, Any]], columns: list[str] | None = None) -> str:
    if not rows:
        return "No rows."
    columns = columns or list(rows[0].keys())
    lines = [
        "| " + " | ".join(columns) + " |",
        "| " + " | ".join(["---"] * len(columns)) + " |",
    ]
    for row in rows:
        values = [str(row.get(column, "N/A")).replace("\n", " ").replace("|", "\\|") for column in columns]
        lines.append("| " + " | ".join(values) + " |")
    return "\n".join(lines)


def completeness_markdown(records: list[dict[str, Any]]) -> str:
    columns = [
        "run_label",
        "expected_total_rows",
        "actual_total_rows",
        "expected_governed_rows",
        "actual_governed_rows",
        "raw_output_present",
        "report_output_present",
        "headline_present",
        "governed_trace_present",
        "artifact_audit_present",
        "provenance_audit_present",
        "rerun_summary_present",
        "senate_summary_present",
        "senate_trace_present",
        "matrix_records_present",
        "run_manifest_present",
        "pack_complete",
        "notes",
    ]
    lines = ["# Aegis Single Run Pack Completeness", "", markdown_table(records, columns), ""]
    for row in records:
        findings = [*row.get("missing_files", []), *row.get("missing_fields", [])]
        if findings:
            lines.extend([f"## {row['run_label']}", ""])
            lines.extend(f"- `{item}`" for item in findings)
            lines.append("")
    return "\n".join(lines)


def grouped_markdown(title: str, rows: list[dict[str, Any]], keys: list[str]) -> str:
    counts = Counter(tuple(row.get(key, "N/A") or "N/A" for key in keys) for row in rows)
    table = [
        {**{key: values[index] for index, key in enumerate(keys)}, "rows": count}
        for values, count in sorted(counts.items())
    ]
    return f"# {title}\n\n{markdown_table(table, [*keys, 'rows'])}"


def split_multi(value: Any) -> list[str]:
    raw = str(value or "").strip()
    if not raw or raw == "N/A":
        return ["N/A"]
    return [item.strip() for item in raw.replace(",", ";").split(";") if item.strip()] or ["N/A"]


def exploded_grouped_markdown(title: str, rows: list[dict[str, Any]], field: str, keys: list[str]) -> str:
    expanded: list[dict[str, Any]] = []
    for row in rows:
        for item in split_multi(row.get(field)):
            expanded.append({**row, field: item})
    return grouped_markdown(title, expanded, [*keys, field])


def zero_or_table(title: str, rows: list[dict[str, Any]], predicate: Callable[[dict[str, Any]], bool], columns: list[str], empty: str) -> str:
    selected = [row for row in rows if predicate(row)]
    if not selected:
        return f"# {title}\n\n{empty}"
    return f"# {title}\n\n{markdown_table(selected, columns)}"


def write_senate_files(out_dir: Path, trace_rows: list[dict[str, Any]], headline: list[dict[str, Any]]) -> None:
    senate_rows = [row for row in trace_rows if is_true(row.get("senate_queued"))]
    senate_columns = [
        "run_label",
        "task_id",
        "task_title",
        "raw_aegis_decision",
        "normalized_decision_bucket",
        "practical_execution_outcome",
        "senate_queued",
        "senate_settled_decision",
        "senate_tally_id",
        "senate_quorum_met",
        "senate_effective_finality",
        "senate_settled_latency_ms",
        "senate_snapshot_joined",
        "mock_tool_applied",
    ]
    write_csv(out_dir / "AEGIS_SINGLE_RUN_SENATE_TRACE.csv", senate_rows, senate_columns)
    write_jsonl(out_dir / "AEGIS_SINGLE_RUN_SENATE_TRACE.jsonl", senate_rows)
    write_md(out_dir / "AEGIS_SINGLE_RUN_SENATE_TRACE.md", "# Aegis Single Run Senate Trace\n\n" + markdown_table(senate_rows, senate_columns))
    write_md(out_dir / "AEGIS_SINGLE_RUN_SENATE_SUMMARY.md", senate_summary_markdown(headline))
    write_md(out_dir / "AEGIS_SINGLE_RUN_SENATE_LATENCY_SUMMARY.md", senate_latency_markdown(senate_rows))


def senate_summary_markdown(headline: list[dict[str, Any]]) -> str:
    rows = [
        {
            "run_label": row["run_label"],
            "initial_senate_escalation_rows": row["initial_senate_escalation_rows"],
            "senate_queued_rows": row["senate_queued_rows"],
            "senate_snapshots_joined": row["senate_snapshots_joined"],
            "senate_settled_allowed_rows": row["senate_settled_allowed_rows"],
            "senate_settled_denied_rows": row["senate_settled_denied_rows"],
            "senate_settled_unknown_rows": row["senate_settled_unknown_rows"],
            "senate_tally_present_rows": row["senate_tally_present_rows"],
            "senate_quorum_met_rows": row["senate_quorum_met_rows"],
            "senate_effective_finality_final_rows": row["senate_effective_finality_final_rows"],
        }
        for row in headline
    ]
    return "\n".join([
        "# Aegis Single Run Senate Summary",
        "",
        "Senate escalation means the Senate voting path. Initial Aegis/PDP responses may be execution-withheld; async settled Senate decisions are reported separately and do not imply mock tool application.",
        "",
        markdown_table(rows),
    ])


def senate_latency_markdown(rows: list[dict[str, Any]]) -> str:
    by_run: dict[str, list[float]] = {}
    for row in rows:
        value = as_float(row.get("senate_settled_latency_ms"))
        if value is not None:
            by_run.setdefault(str(row.get("run_label", "N/A")), []).append(value)
    if not by_run:
        return "# Aegis Single Run Senate Latency Summary\n\nN/A: no Senate settlement latency values were available."
    table = []
    for run, values in sorted(by_run.items()):
        ordered = sorted(values)
        table.append({
            "run_label": run,
            "rows": len(ordered),
            "min_ms": round(ordered[0], 3),
            "p50_ms": round(percentile(ordered, 50), 3),
            "mean_ms": round(mean(ordered), 3),
            "p90_ms": round(percentile(ordered, 90), 3),
            "p95_ms": round(percentile(ordered, 95), 3),
            "p99_ms": round(percentile(ordered, 99), 3),
            "max_ms": round(ordered[-1], 3),
        })
    return "# Aegis Single Run Senate Latency Summary\n\n" + markdown_table(table)


def percentile(values: list[float], pct: float) -> float:
    if not values:
        return 0.0
    idx = min(len(values) - 1, max(0, round((pct / 100) * (len(values) - 1))))
    return values[idx]


def provenance_markdown(headline: list[dict[str, Any]]) -> str:
    rows = [
        {
            "run_label": row["run_label"],
            "evidence_complete_rows": row["evidence_complete_rows"],
            "evidence_completeness_rate": row["evidence_completeness_rate"],
            "trusted_aegis_resolved_provenance_rows": row["trusted_aegis_resolved_provenance_rows"],
            "provenance_unknown_rows": row["provenance_unknown_rows"],
            "provenance_invalid_rows": row["provenance_invalid_rows"],
            "local_fail_closed_no_tool_rows": row["local_fail_closed_no_tool_rows"],
        }
        for row in headline
    ]
    return "\n".join([
        "# Aegis Single Run Provenance Summary",
        "",
        "Evidence completeness is separate from trusted Aegis-resolved provenance. Local fail-closed/no-tool rows are not counted as invalid provenance simply because Aegis was not attempted.",
        "",
        markdown_table(rows),
    ])


def provenance_by_run_markdown(headline: list[dict[str, Any]]) -> str:
    return "# Aegis Single Run Provenance By Run\n\n" + markdown_table(headline, [
        "run_label",
        "aegis_attempted_rows",
        "trusted_aegis_resolved_provenance_rows",
        "provenance_unknown_rows",
        "provenance_invalid_rows",
    ])


def risk_markdown(headline: list[dict[str, Any]], leakage_rows: list[dict[str, str]]) -> str:
    leakage_by_run = Counter(row.get("run_label", "") for row in leakage_rows)
    rows = [
        {
            "run_label": row["run_label"],
            "governed_rows": row["governed_rows"],
            "mock_tool_applied_rows": row["mock_tool_applied_rows"],
            "governed_risky_side_effect_completions": row["governed_risky_side_effect_completions"],
            "prompt_policy_leakage_counterfactual_rows": leakage_by_run[row["run_label"]],
        }
        for row in headline
    ]
    return "# Aegis Single Run Risk Outcome Summary\n\n" + markdown_table(rows)


def write_action_tables(out_dir: Path, rows: list[dict[str, Any]]) -> None:
    specs = [
        ("AEGIS_SINGLE_RUN_ALLOWED_OR_APPROVED_ACTIONS.md", "Aegis Single Run Allowed Or Approved Actions", lambda r: r.get("normalized_decision_bucket") == "allow_or_approve"),
        ("AEGIS_SINGLE_RUN_BLOCKED_ACTIONS.md", "Aegis Single Run Blocked Actions", lambda r: r.get("normalized_decision_bucket") == "block"),
        ("AEGIS_SINGLE_RUN_EXECUTION_WITHHELD_ACTIONS.md", "Aegis Single Run Execution Withheld Actions", lambda r: r.get("normalized_decision_bucket") == "execution_withheld" or r.get("practical_execution_outcome") in {"execution_withheld", "senate_voting_pending"}),
        ("AEGIS_SINGLE_RUN_FAIL_CLOSED_NO_ACTIONS.md", "Aegis Single Run Fail Closed No Actions", lambda r: r.get("normalized_decision_bucket") == "fail_closed_no_action"),
        ("AEGIS_SINGLE_RUN_OTHER_OR_UNKNOWN_DECISIONS.md", "Aegis Single Run Other Or Unknown Decisions", lambda r: r.get("normalized_decision_bucket") in {"other", "parser_or_backend_failure"}),
    ]
    columns = ["run_label", "task_id", "task_title", "proposed_mock_tool", "aegis_decision", "normalized_decision_bucket", "practical_execution_outcome", "senate_settled_decision"]
    for file_name, title, predicate in specs:
        write_md(out_dir / file_name, zero_or_table(title, rows, predicate, columns, f"No rows matched `{title}`."))


def rerun_markdown(headline: list[dict[str, Any]], completeness: list[dict[str, Any]]) -> str:
    rows = [
        {
            "run_label": row["run_label"],
            "pack_complete": row["pack_complete"],
            "rerun_recommended": row["rerun_recommended"],
            "rerun_needed_for_risk_outcome_claims": row["rerun_needed_for_risk_outcome_claims"],
            "rerun_needed_for_provenance_claims": row["rerun_needed_for_provenance_claims"],
            "rerun_needed_for_full_paper_claims": row["rerun_needed_for_full_paper_claims"],
            "rerun_reason_short": row["rerun_reason_short"],
        }
        for row in headline
    ]
    missing = [row["run_label"] for row in completeness if not is_true(row.get("pack_complete"))]
    verdict = "No rerun recommended." if not missing and all(str(row["rerun_recommended"]).lower() in {"no_rerun_needed", "false", "no"} for row in headline) else "Rerun or manual review needed; see table."
    return "# Aegis Single Run Rerun Readiness Summary\n\n" + verdict + "\n\n" + markdown_table(rows)


def paper_readiness_markdown(headline: list[dict[str, Any]], completeness: list[dict[str, Any]], aggregates: dict[str, Any]) -> str:
    complete = {row["run_label"]: is_true(row.get("pack_complete")) for row in completeness}
    rows = []
    for row in headline:
        ready = (
            complete.get(row["run_label"], False)
            and as_int(row["governed_risky_side_effect_completions"]) == 0
            and as_int(row["provenance_unknown_rows"]) == 0
            and as_int(row["provenance_invalid_rows"]) == 0
            and str(row["rerun_recommended"]).lower() in {"no_rerun_needed", "false", "no"}
        )
        rows.append({
            "run_label": row["run_label"],
            "pack_complete": complete.get(row["run_label"], False),
            "paper_ready": ready,
            "rerun_reason_short": row["rerun_reason_short"],
        })
    return "\n".join([
        "# Aegis Single Run Paper Readiness",
        "",
        f"- Overall single-run comparison pack complete: `{aggregates['overall_pack_complete']}`",
        f"- Overall single-run comparison paper-ready: `{aggregates['overall_paper_ready']}`",
        "- Senate escalation means Senate voting path, not a generic manual-review path.",
        "- Settled Senate decisions are reported separately from initial execution-withheld Aegis/PDP decisions.",
        "",
        markdown_table(rows),
    ])


def write_index(out_dir: Path) -> None:
    descriptions = {
        "AEGIS_SINGLE_RUN_HEADLINE.md": "Headline per-run counts and paper-readiness fields.",
        "AEGIS_SINGLE_RUN_GOVERNED_DECISION_TRACE.csv": "Combined governed trace across all five single runs.",
        "AEGIS_SINGLE_RUN_PACK_COMPLETENESS.md": "Per-pack artifact and field completeness audit.",
        "AEGIS_SINGLE_RUN_SENATE_SUMMARY.md": "Initial Senate path, settled decision, quorum, tally, and finality summary.",
        "AEGIS_SINGLE_RUN_PROVENANCE_SUMMARY.md": "Evidence completeness and trusted Aegis-resolved provenance summary.",
        "AEGIS_SINGLE_RUN_RISK_OUTCOME_SUMMARY.md": "Mock-tool application and risky side-effect completion summary.",
        "AEGIS_SINGLE_RUN_PAPER_READINESS.md": "Paper-readiness verdict per run and overall.",
    }
    lines = [
        "# Single Run Comparison Report Index",
        "",
        "This directory is generated from existing one-run artifacts under `reports/One Run Folder`. It does not rerun models or call Aegis/backend services.",
        "",
    ]
    for path in sorted(out_dir.iterdir()):
        if path.is_file():
            lines.append(f"- `{path.name}`: {descriptions.get(path.name, 'Detailed generated table or machine-readable companion file.')}")
    write_md(out_dir / "REPORT_INDEX.md", "\n".join(lines))


def write_top_report(top_report: Path, headline: list[dict[str, Any]], completeness: list[dict[str, Any]], aggregates: dict[str, Any]) -> None:
    completeness_rows = [
        {
            "run_label": row["run_label"],
            "total_rows": row["actual_total_rows"],
            "governed_rows": row["actual_governed_rows"],
            "pack_complete": row["pack_complete"],
        }
        for row in completeness
    ]
    headline_rows = [
        {
            "run_label": row["run_label"],
            "total_rows": row["total_rows"],
            "governed_rows": row["governed_rows"],
            "aegis_attempted_rows": row["aegis_attempted_rows"],
            "local_fail_closed_no_tool_rows": row["local_fail_closed_no_tool_rows"],
            "initial_execution_withheld_rows": row["initial_execution_withheld_rows"],
            "senate_queued_rows": row["senate_queued_rows"],
            "senate_settled_allowed_rows": row["senate_settled_allowed_rows"],
            "senate_settled_denied_rows": row["senate_settled_denied_rows"],
            "mock_tool_applied_rows": row["mock_tool_applied_rows"],
            "risk_completions": row["governed_risky_side_effect_completions"],
            "trusted_provenance_rows": row["trusted_aegis_resolved_provenance_rows"],
        }
        for row in headline
    ]
    lines = [
        "# Single Run Comparison Report",
        "",
        "## Executive Summary",
        "",
        f"- Included rows: `{aggregates['total_rows']}` total rows across five single-run packs.",
        f"- Governed rows: `{aggregates['governed_rows']}`.",
        f"- Aegis-attempted governed rows: `{aggregates['aegis_attempted_rows']}`.",
        f"- Local fail-closed/no-tool rows: `{aggregates['local_fail_closed_no_tool_rows']}`.",
        f"- Initial execution-withheld rows: `{aggregates['initial_execution_withheld_rows']}`.",
        f"- Senate queued rows: `{aggregates['senate_queued_rows']}`.",
        f"- Senate settled allowed rows: `{aggregates['senate_settled_allowed_rows']}`.",
        f"- Senate settled denied rows: `{aggregates['senate_settled_denied_rows']}`.",
        f"- Final signed tally rows: `{aggregates['senate_tally_present_rows']}`.",
        f"- Quorum-met rows: `{aggregates['senate_quorum_met_rows']}`.",
        f"- Governed mock tool applications: `{aggregates['mock_tool_applied_rows']}`.",
        f"- Governed risky side-effect completions: `{aggregates['governed_risky_side_effect_completions']}`.",
        f"- Trusted Aegis-resolved provenance rows: `{aggregates['trusted_aegis_resolved_provenance_rows']}`.",
        f"- Provenance unknown rows: `{aggregates['provenance_unknown_rows']}`.",
        f"- Provenance invalid rows: `{aggregates['provenance_invalid_rows']}`.",
        f"- Prompt-policy leakage counterfactual rows: `{aggregates['prompt_policy_leakage_rows']}`.",
        f"- Single-run pack complete: `{aggregates['overall_pack_complete']}`.",
        f"- Any run needs rerun: `{not aggregates['overall_paper_ready']}`.",
        f"- Senate status joined where applicable: `{aggregates['senate_queued_rows'] == aggregates['senate_tally_present_rows'] == aggregates['senate_quorum_met_rows']}`.",
        f"- Single-run set ready for paper tables: `{aggregates['overall_paper_ready']}`.",
        "",
        "## Input Runs Included",
        "",
        markdown_table(completeness_rows),
        "",
        "## Pack Completeness Status",
        "",
        "See `single_run_report/AEGIS_SINGLE_RUN_PACK_COMPLETENESS.md`.",
        "",
        "## Headline Comparison Table",
        "",
        markdown_table(headline_rows),
        "",
        "## Governed Decision Comparison",
        "",
        "See `single_run_report/AEGIS_SINGLE_RUN_GOVERNED_DECISION_TRACE.md`, `AEGIS_SINGLE_RUN_BY_DECISION_BUCKET.md`, and `AEGIS_SINGLE_RUN_PRACTICAL_EXECUTION_OUTCOMES.md`.",
        "",
        "## Senate Settled Outcome Comparison",
        "",
        "Senate escalation means Senate voting path. The report preserves initial Aegis/PDP response, queued state, async settled decision, finality, quorum, tally ID presence, and latency.",
        "",
        "See `single_run_report/AEGIS_SINGLE_RUN_SENATE_SUMMARY.md` and `AEGIS_SINGLE_RUN_SENATE_LATENCY_SUMMARY.md`.",
        "",
        "## Provenance Comparison",
        "",
        "Evidence completeness is distinct from trusted Aegis-resolved provenance. Client/PEP-supplied citations are not counted as production-valid policy evidence.",
        "",
        "See `single_run_report/AEGIS_SINGLE_RUN_PROVENANCE_SUMMARY.md` and `AEGIS_SINGLE_RUN_PROVENANCE_BOUNDARY_AUDIT.md`.",
        "",
        "## Risk Outcome Comparison",
        "",
        "A settled Senate `allow` does not mean the original mock tool was applied unless `mock_tool_applied=true`.",
        "",
        "See `single_run_report/AEGIS_SINGLE_RUN_RISK_OUTCOME_SUMMARY.md`, `AEGIS_SINGLE_RUN_RISKY_COMPLETIONS.md`, `AEGIS_SINGLE_RUN_MOCK_TOOL_APPLICATIONS.md`, `PROMPT_POLICY_LEAKAGE_WITH_AEGIS_COUNTERFACTUAL.md`, and `PROMPT_POLICY_LEAKAGE_EVENT_CHAIN.md`.",
        "",
        "## Tool/Control/Workflow Comparison",
        "",
        "See `AEGIS_SINGLE_RUN_BY_TOOL_AND_BUCKET.md`, `AEGIS_SINGLE_RUN_BY_CONTROL_AND_BUCKET.md`, `AEGIS_SINGLE_RUN_BY_WORKFLOW_AND_BUCKET.md`, `AEGIS_SINGLE_RUN_BY_FAILURE_CATEGORY.md`, and `AEGIS_SINGLE_RUN_BY_TASK.md`.",
        "",
        "## Expected-vs-Actual Summary",
        "",
        "See `single_run_report/AEGIS_SINGLE_RUN_EXPECTED_VS_ACTUAL.md`.",
        "",
        "## Rerun/Readiness Verdict",
        "",
        "See `single_run_report/AEGIS_SINGLE_RUN_RERUN_READINESS_SUMMARY.md` and `AEGIS_SINGLE_RUN_PAPER_READINESS.md`.",
        "",
        "## Interpretation Notes",
        "",
        "- Raw Aegis decision, normalized decision bucket, practical execution outcome, and settled Senate decision are separate fields.",
        "- Senate escalation means Senate voting path, not a generic manual-review path.",
        "- Settled Senate allow is a governance settlement, not proof that the original mock tool was applied.",
        "- Local fail-closed/no-tool rows where Aegis was not attempted are not counted as invalid provenance.",
        "- This pack was generated from existing artifacts only. It did not rerun models, call Aegis/backend services, mutate policy, mutate prompts, or perform side effects.",
        "",
        "## Detailed Tables",
        "",
        "- `single_run_report/REPORT_INDEX.md`",
        "- `single_run_report/AEGIS_SINGLE_RUN_HEADLINE.md`",
        "- `single_run_report/AEGIS_SINGLE_RUN_GOVERNED_DECISION_TRACE.md`",
        "- `single_run_report/AEGIS_SINGLE_RUN_SENATE_SUMMARY.md`",
        "- `single_run_report/AEGIS_SINGLE_RUN_PROVENANCE_SUMMARY.md`",
        "- `single_run_report/AEGIS_SINGLE_RUN_RISK_OUTCOME_SUMMARY.md`",
        "- `single_run_report/AEGIS_SINGLE_RUN_PAPER_READINESS.md`",
    ]
    write_md(top_report, "\n".join(lines))


def rel(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


if __name__ == "__main__":
    raise SystemExit(main())
