#!/usr/bin/env python3
from __future__ import annotations

import csv
import json
import shutil
from collections import Counter
from pathlib import Path
from statistics import mean
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
PACK_DIR = ROOT / "reports" / "10 Run Folder" / "10 run comparison"
SOURCE_REPORT = PACK_DIR / "comparison_report"
OUT_DIR = PACK_DIR / "ten_run_report"
TOP_REPORT = PACK_DIR / "TEN_RUN_COMPARISON_REPORT.md"

RUN_PACKS = [
    {
        "run_label": "stubbed_10_run",
        "display": "Stubbed 10x",
        "pack": ROOT / "reports" / "10 Run Folder" / "Stubbed 10 run",
        "raw": "stubbed_output",
        "report": "stubbed_report",
    },
    {
        "run_label": "gemma_10_run",
        "display": "Gemma 10x",
        "pack": ROOT / "reports" / "10 Run Folder" / "Gemma 10 run",
        "raw": "gemma_output",
        "report": "gemma_report",
    },
    {
        "run_label": "frontier_temp_0_10_run",
        "display": "Frontier temp 0 10x",
        "pack": ROOT / "reports" / "10 Run Folder" / "Frontier temp 0 10 run",
        "raw": "frontier_output",
        "report": "frontier_report",
    },
    {
        "run_label": "frontier_temp_0.7_10_run",
        "display": "Frontier temp 0.7 10x",
        "pack": ROOT / "reports" / "10 Run Folder" / "Frontier temp 0.7 10 run",
        "raw": "frontier_output",
        "report": "frontier_report",
    },
    {
        "run_label": "frontier_temp_1.0_10_run",
        "display": "Frontier temp 1.0 10x",
        "pack": ROOT / "reports" / "10 Run Folder" / "Frontier temp 1.0 10 run",
        "raw": "frontier_output",
        "report": "frontier_report",
    },
]

EXPECTED_TOTAL_ROWS = 1260
EXPECTED_GOVERNED_ROWS = 420

RENAMED_REPORTS = {
    "AEGIS_GOVERNED_DECISION_HEADLINE.md": "AEGIS_10_RUN_HEADLINE.md",
    "AEGIS_GOVERNED_DECISION_HEADLINE.csv": "AEGIS_10_RUN_HEADLINE.csv",
    "AEGIS_GOVERNED_DECISION_HEADLINE.json": "AEGIS_10_RUN_HEADLINE.json",
    "AEGIS_GOVERNED_DECISION_TRACE.md": "AEGIS_10_RUN_GOVERNED_DECISION_TRACE.md",
    "AEGIS_GOVERNED_DECISION_TRACE.csv": "AEGIS_10_RUN_GOVERNED_DECISION_TRACE.csv",
    "AEGIS_GOVERNED_DECISION_TRACE.jsonl": "AEGIS_10_RUN_GOVERNED_DECISION_TRACE.jsonl",
    "AEGIS_DECISION_BY_RUN_AND_BUCKET.md": "AEGIS_10_RUN_BY_DECISION_BUCKET.md",
    "AEGIS_DECISION_BY_EXPECTED_OUTCOME.md": "AEGIS_10_RUN_BY_EXPECTED_OUTCOME.md",
    "AEGIS_EXPECTED_VS_ACTUAL_DECISION_MATCH.md": "AEGIS_10_RUN_EXPECTED_VS_ACTUAL.md",
    "AEGIS_PRACTICAL_EXECUTION_OUTCOMES.md": "AEGIS_10_RUN_PRACTICAL_EXECUTION_OUTCOMES.md",
    "AEGIS_SENATE_ASYNC_STATUS_SUMMARY.md": "AEGIS_10_RUN_SENATE_SUMMARY.md",
    "AEGIS_SENATE_ASYNC_STATUS_TRACE.csv": "AEGIS_10_RUN_SENATE_TRACE.csv",
    "AEGIS_SENATE_ASYNC_STATUS_TRACE.md": "AEGIS_10_RUN_SENATE_TRACE.md",
    "AEGIS_SENATE_ASYNC_STATUS_TRACE.jsonl": "AEGIS_10_RUN_SENATE_TRACE.jsonl",
    "AEGIS_SENATE_BY_SETTLED_DECISION.md": "AEGIS_10_RUN_SENATE_BY_SETTLED_DECISION.md",
    "AEGIS_SENATE_SETTLED_ALLOWED_ACTIONS.md": "AEGIS_10_RUN_SENATE_SETTLED_ALLOWED_ACTIONS.md",
    "AEGIS_SENATE_SETTLED_DENIED_ACTIONS.md": "AEGIS_10_RUN_SENATE_SETTLED_DENIED_ACTIONS.md",
    "AEGIS_PROVENANCE_BOUNDARY_AUDIT.md": "AEGIS_10_RUN_PROVENANCE_BOUNDARY_AUDIT.md",
    "AEGIS_DECISION_BY_TOOL_AND_BUCKET.md": "AEGIS_10_RUN_BY_TOOL_AND_BUCKET.md",
    "AEGIS_DECISION_BY_CONTROL_AND_BUCKET.md": "AEGIS_10_RUN_BY_CONTROL_AND_BUCKET.md",
    "AEGIS_BLOCKED_ACTIONS.md": "AEGIS_10_RUN_BLOCKED_ACTIONS.md",
    "AEGIS_EXECUTION_WITHHELD_ACTIONS.md": "AEGIS_10_RUN_EXECUTION_WITHHELD_ACTIONS.md",
    "AEGIS_FAIL_CLOSED_NO_ACTIONS.md": "AEGIS_10_RUN_FAIL_CLOSED_NO_ACTIONS.md",
    "AEGIS_ALLOWED_OR_APPROVED_ACTIONS.md": "AEGIS_10_RUN_ALLOWED_OR_APPROVED_ACTIONS.md",
    "AEGIS_OTHER_OR_UNKNOWN_DECISIONS.md": "AEGIS_10_RUN_OTHER_OR_UNKNOWN_DECISIONS.md",
    "PROMPT_POLICY_LEAKAGE_WITH_AEGIS_COUNTERFACTUAL.md": "PROMPT_POLICY_LEAKAGE_WITH_AEGIS_COUNTERFACTUAL.md",
    "PROMPT_POLICY_LEAKAGE_WITH_AEGIS_COUNTERFACTUAL.csv": "PROMPT_POLICY_LEAKAGE_WITH_AEGIS_COUNTERFACTUAL.csv",
    "PROMPT_POLICY_LEAKAGE_WITH_AEGIS_COUNTERFACTUAL.jsonl": "PROMPT_POLICY_LEAKAGE_WITH_AEGIS_COUNTERFACTUAL.jsonl",
    "PROMPT_POLICY_LEAKAGE_EVENT_CHAIN.md": "PROMPT_POLICY_LEAKAGE_EVENT_CHAIN.md",
    "PROMPT_POLICY_LEAKAGE_EVENT_CHAIN.csv": "PROMPT_POLICY_LEAKAGE_EVENT_CHAIN.csv",
    "PROMPT_POLICY_LEAKAGE_EVENT_CHAIN.jsonl": "PROMPT_POLICY_LEAKAGE_EVENT_CHAIN.jsonl",
}


def main() -> int:
    if not SOURCE_REPORT.exists():
        raise SystemExit(f"Missing source comparison report: {SOURCE_REPORT}")

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    for src_name, dest_name in RENAMED_REPORTS.items():
        src = SOURCE_REPORT / src_name
        if src.exists():
            shutil.copy2(src, OUT_DIR / dest_name)

    normalized_rows = read_csv(SOURCE_REPORT / "normalized_results.csv")
    governed_rows = read_csv(SOURCE_REPORT / "AEGIS_GOVERNED_DECISION_TRACE.csv")
    headline_rows = read_csv(SOURCE_REPORT / "AEGIS_GOVERNED_DECISION_HEADLINE.csv")
    senate_rows = read_csv(SOURCE_REPORT / "AEGIS_SENATE_ASYNC_STATUS_SUMMARY.csv")
    leakage_rows = read_csv(SOURCE_REPORT / "PROMPT_POLICY_LEAKAGE_WITH_AEGIS_COUNTERFACTUAL.csv")

    completeness = build_completeness(normalized_rows, governed_rows)
    write_json(OUT_DIR / "AEGIS_10_RUN_PACK_COMPLETENESS.json", completeness)
    write_md(OUT_DIR / "AEGIS_10_RUN_PACK_COMPLETENESS.md", completeness_markdown(completeness))

    aggregates = build_aggregates(normalized_rows, governed_rows, headline_rows, senate_rows, leakage_rows)
    write_json(OUT_DIR / "AEGIS_10_RUN_PAPER_READINESS.json", aggregates)
    write_md(OUT_DIR / "AEGIS_10_RUN_PAPER_READINESS.md", paper_readiness_markdown(aggregates, completeness))
    write_md(OUT_DIR / "AEGIS_10_RUN_RERUN_READINESS_SUMMARY.md", rerun_markdown(aggregates, completeness))
    write_md(OUT_DIR / "AEGIS_10_RUN_RISK_OUTCOME_SUMMARY.md", risk_markdown(aggregates))
    write_md(OUT_DIR / "AEGIS_10_RUN_PROVENANCE_SUMMARY.md", provenance_markdown(aggregates))
    write_md(OUT_DIR / "AEGIS_10_RUN_MOCK_TOOL_APPLICATIONS.md", zero_or_table(
        "Aegis-Governed Mock Tool Applications",
        governed_rows,
        lambda row: is_true(row.get("mock_tool_applied")),
        ["run_label", "task_id", "task_title", "proposed_mock_tool", "aegis_decision", "practical_execution_outcome"],
        "No governed mock tool applications found in the 10x comparison.",
    ))
    write_md(OUT_DIR / "AEGIS_10_RUN_RISKY_COMPLETIONS.md", zero_or_table(
        "Aegis-Governed Risky Side-Effect Completions",
        governed_rows,
        lambda row: is_true(row.get("governed_risky_side_effect_completed")),
        ["run_label", "task_id", "task_title", "proposed_mock_tool", "aegis_decision", "practical_execution_outcome"],
        "No governed risky side-effect completions found in the 10x comparison.",
    ))
    write_md(OUT_DIR / "AEGIS_10_RUN_BY_WORKFLOW_AND_BUCKET.md", grouped_markdown(
        "10x By Workflow And Decision Bucket",
        governed_rows,
        ["run_label", "workflow_family", "normalized_decision_bucket"],
    ))
    write_md(OUT_DIR / "AEGIS_10_RUN_BY_FAILURE_CATEGORY.md", grouped_markdown(
        "10x By Failure Category",
        governed_rows,
        ["run_label", "failure_category", "normalized_decision_bucket"],
    ))
    write_md(OUT_DIR / "AEGIS_10_RUN_BY_TASK.md", grouped_markdown(
        "10x By Task",
        governed_rows,
        ["run_label", "task_id", "task_title", "normalized_decision_bucket"],
    ))
    write_md(OUT_DIR / "AEGIS_10_RUN_SENATE_LATENCY_SUMMARY.md", senate_latency_markdown(governed_rows))
    write_md(OUT_DIR / "AEGIS_10_RUN_PROVENANCE_BY_RUN.md", provenance_by_run_markdown(headline_rows))
    write_index()
    write_top_report(aggregates, completeness)

    print(json.dumps({
        "output_dir": str(PACK_DIR),
        "top_report": str(TOP_REPORT),
        "detail_report_dir": str(OUT_DIR),
        "total_rows": aggregates["total_rows"],
        "governed_rows": aggregates["governed_rows"],
        "pack_complete": aggregates["overall_pack_complete"],
    }, indent=2, sort_keys=True))
    return 0


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def write_json(path: Path, payload: Any) -> None:
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


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


def build_completeness(normalized_rows: list[dict[str, str]], governed_rows: list[dict[str, str]]) -> list[dict[str, Any]]:
    by_run_total = Counter(row.get("run_label", "") for row in normalized_rows)
    by_run_governed = Counter(row.get("run_label", "") for row in governed_rows)
    records: list[dict[str, Any]] = []
    required_report_files = [
        "AEGIS_GOVERNED_DECISION_HEADLINE.csv",
        "AEGIS_GOVERNED_DECISION_TRACE.csv",
        "AEGIS_ARTIFACT_AUDIT.json",
        "AEGIS_PROVENANCE_BOUNDARY_AUDIT.json",
        "AEGIS_RERUN_READINESS_SUMMARY.md",
        "AEGIS_SENATE_ASYNC_STATUS_SUMMARY.csv",
        "AEGIS_SENATE_ASYNC_STATUS_TRACE.csv",
        "PROMPT_POLICY_LEAKAGE_WITH_AEGIS_COUNTERFACTUAL.csv",
        "PROMPT_POLICY_LEAKAGE_EVENT_CHAIN.csv",
        "REPORT_INDEX.md",
    ]
    for spec in RUN_PACKS:
        pack = spec["pack"]
        raw_dir = pack / spec["raw"]
        report_dir = pack / spec["report"]
        matrix_files = sorted(raw_dir.glob("loop_*/matrix_records.jsonl"))
        manifest_files = sorted(raw_dir.glob("loop_*/run_manifest.json"))
        missing_files: list[str] = []
        if not raw_dir.exists():
            missing_files.append(str(raw_dir.relative_to(ROOT)))
        if not report_dir.exists():
            missing_files.append(str(report_dir.relative_to(ROOT)))
        if len(matrix_files) != 10:
            missing_files.append(f"{raw_dir.relative_to(ROOT)}/loop_*/matrix_records.jsonl (expected 10)")
        if len(manifest_files) != 10:
            missing_files.append(f"{raw_dir.relative_to(ROOT)}/loop_*/run_manifest.json (expected 10)")
        for file_name in required_report_files:
            if not (report_dir / file_name).exists():
                missing_files.append(str((report_dir / file_name).relative_to(ROOT)))
        total = by_run_total[spec["run_label"]]
        governed = by_run_governed[spec["run_label"]]
        if total != EXPECTED_TOTAL_ROWS:
            missing_files.append(f"total rows expected {EXPECTED_TOTAL_ROWS}, observed {total}")
        if governed != EXPECTED_GOVERNED_ROWS:
            missing_files.append(f"governed rows expected {EXPECTED_GOVERNED_ROWS}, observed {governed}")
        records.append({
            "run_label": spec["run_label"],
            "display_label": spec["display"],
            "expected_total_rows": EXPECTED_TOTAL_ROWS,
            "actual_total_rows": total,
            "expected_governed_rows": EXPECTED_GOVERNED_ROWS,
            "actual_governed_rows": governed,
            "raw_output_present": raw_dir.exists(),
            "report_output_present": report_dir.exists(),
            "matrix_record_files": len(matrix_files),
            "run_manifest_files": len(manifest_files),
            "pack_complete": not missing_files,
            "missing_files_or_findings": missing_files,
            "notes": "Complete 10-loop pack." if not missing_files else "See missing_files_or_findings.",
        })
    return records


def build_aggregates(
    normalized_rows: list[dict[str, str]],
    governed_rows: list[dict[str, str]],
    headline_rows: list[dict[str, str]],
    senate_rows: list[dict[str, str]],
    leakage_rows: list[dict[str, str]],
) -> dict[str, Any]:
    headline_by_run = {row.get("run_label", ""): row for row in headline_rows}
    senate_by_run = {row.get("run_label", ""): row for row in senate_rows}
    run_rows = []
    for spec in RUN_PACKS:
        run = spec["run_label"]
        h = headline_by_run.get(run, {})
        s = senate_by_run.get(run, {})
        total_rows = sum(1 for row in normalized_rows if row.get("run_label") == run)
        run_rows.append({
            "run_label": run,
            "display_label": spec["display"],
            "total_rows": total_rows,
            "governed_rows": as_int(h.get("governed_rows")),
            "aegis_attempted_rows": as_int(h.get("aegis_attempted_rows")),
            "local_fail_closed_no_tool_rows": as_int(h.get("fail_closed_no_action_rows")),
            "initial_execution_withheld_rows": as_int(h.get("execution_withheld_rows")),
            "initial_senate_escalation_rows": as_int(h.get("senate_escalation_rows")),
            "senate_queued_rows": as_int(s.get("senate_rows")),
            "senate_snapshots_joined": as_int(s.get("snapshot_rows")),
            "senate_settled_allowed_rows": as_int(s.get("settled_allowed_rows")),
            "senate_settled_denied_rows": as_int(s.get("settled_denied_rows")),
            "senate_tally_present_rows": as_int(s.get("tally_present_rows")),
            "senate_quorum_met_rows": as_int(s.get("quorum_met_rows")),
            "mock_tool_applied_rows": as_int(h.get("mock_tool_applied_rows")),
            "governed_risky_side_effect_completions": as_int(h.get("governed_risky_side_effect_completions")),
            "trusted_aegis_resolved_provenance_rows": as_int(h.get("provenance_boundary_valid_rows")),
            "provenance_unknown_rows": as_int(h.get("provenance_boundary_unknown_rows")),
            "provenance_invalid_rows": as_int(h.get("provenance_boundary_invalid_rows")),
            "prompt_policy_leakage_rows": sum(1 for row in leakage_rows if row.get("run_label") == run),
            "rerun_recommended": h.get("rerun_recommended", "unknown"),
            "rerun_reason_short": h.get("rerun_reason_short", "N/A"),
        })
    totals = {
        "total_rows": len(normalized_rows),
        "governed_rows": sum(row["governed_rows"] for row in run_rows),
        "aegis_attempted_rows": sum(row["aegis_attempted_rows"] for row in run_rows),
        "local_fail_closed_no_tool_rows": sum(row["local_fail_closed_no_tool_rows"] for row in run_rows),
        "initial_execution_withheld_rows": sum(row["initial_execution_withheld_rows"] for row in run_rows),
        "senate_queued_rows": sum(row["senate_queued_rows"] for row in run_rows),
        "senate_settled_allowed_rows": sum(row["senate_settled_allowed_rows"] for row in run_rows),
        "senate_settled_denied_rows": sum(row["senate_settled_denied_rows"] for row in run_rows),
        "senate_tally_present_rows": sum(row["senate_tally_present_rows"] for row in run_rows),
        "senate_quorum_met_rows": sum(row["senate_quorum_met_rows"] for row in run_rows),
        "mock_tool_applied_rows": sum(row["mock_tool_applied_rows"] for row in run_rows),
        "governed_risky_side_effect_completions": sum(row["governed_risky_side_effect_completions"] for row in run_rows),
        "trusted_aegis_resolved_provenance_rows": sum(row["trusted_aegis_resolved_provenance_rows"] for row in run_rows),
        "provenance_unknown_rows": sum(row["provenance_unknown_rows"] for row in run_rows),
        "provenance_invalid_rows": sum(row["provenance_invalid_rows"] for row in run_rows),
        "prompt_policy_leakage_rows": len(leakage_rows),
    }
    no_rerun_values = {"no", "false", "n/a", "", "no_rerun_needed"}
    return {
        "runs": run_rows,
        **totals,
        "overall_pack_complete": all(row["total_rows"] == EXPECTED_TOTAL_ROWS and row["governed_rows"] == EXPECTED_GOVERNED_ROWS for row in run_rows),
        "overall_paper_ready": all(str(row["rerun_recommended"]).strip().lower() in no_rerun_values for row in run_rows)
        and totals["governed_risky_side_effect_completions"] == 0
        and totals["provenance_invalid_rows"] == 0,
    }


def markdown_table(rows: list[dict[str, Any]], columns: list[str] | None = None) -> str:
    if not rows:
        return ""
    columns = columns or list(rows[0].keys())
    lines = [
        "| " + " | ".join(columns) + " |",
        "| " + " | ".join(["---"] * len(columns)) + " |",
    ]
    for row in rows:
        values = [str(row.get(column, "N/A")).replace("\n", " ") for column in columns]
        lines.append("| " + " | ".join(values) + " |")
    return "\n".join(lines)


def completeness_markdown(records: list[dict[str, Any]]) -> str:
    rows = [
        {
            "run_label": row["run_label"],
            "actual_total_rows": row["actual_total_rows"],
            "actual_governed_rows": row["actual_governed_rows"],
            "matrix_record_files": row["matrix_record_files"],
            "run_manifest_files": row["run_manifest_files"],
            "pack_complete": row["pack_complete"],
            "notes": row["notes"],
        }
        for row in records
    ]
    lines = ["# Aegis 10 Run Pack Completeness", "", markdown_table(rows), ""]
    for row in records:
        if row["missing_files_or_findings"]:
            lines.extend([f"## {row['run_label']}", ""])
            lines.extend(f"- `{item}`" for item in row["missing_files_or_findings"])
            lines.append("")
    return "\n".join(lines)


def paper_readiness_markdown(aggregates: dict[str, Any], completeness: list[dict[str, Any]]) -> str:
    rows = []
    complete_by_run = {row["run_label"]: row["pack_complete"] for row in completeness}
    for row in aggregates["runs"]:
        ready = complete_by_run.get(row["run_label"], False) and row["governed_risky_side_effect_completions"] == 0 and row["provenance_invalid_rows"] == 0
        rows.append({
            "run_label": row["run_label"],
            "pack_complete": complete_by_run.get(row["run_label"], False),
            "paper_ready": ready,
            "risk_completions": row["governed_risky_side_effect_completions"],
            "provenance_valid": row["trusted_aegis_resolved_provenance_rows"],
            "provenance_unknown": row["provenance_unknown_rows"],
            "provenance_invalid": row["provenance_invalid_rows"],
            "rerun_reason": row["rerun_reason_short"],
        })
    return "\n".join([
        "# Aegis 10 Run Paper Readiness",
        "",
        f"- Overall pack complete: `{aggregates['overall_pack_complete']}`",
        f"- Overall paper-ready verdict: `{aggregates['overall_paper_ready']}`",
        "- Senate escalation means Senate voting path / execution withheld pending scoped signed tally where applicable.",
        "- Settled Senate allow is reported separately from initial Aegis/PDP execution-withheld decisions and does not imply a mock tool was applied.",
        "",
        markdown_table(rows),
    ])


def rerun_markdown(aggregates: dict[str, Any], completeness: list[dict[str, Any]]) -> str:
    missing = [row for row in completeness if not row["pack_complete"]]
    lines = [
        "# Aegis 10 Run Rerun Readiness Summary",
        "",
        f"- Existing 10x artifacts sufficient for report regeneration: `{not missing}`",
        f"- Rerun needed for governed risk-outcome claims: `{aggregates['governed_risky_side_effect_completions'] != 0}`",
        f"- Rerun needed for trusted provenance/source-mapping claims: `{aggregates['provenance_invalid_rows'] != 0}`",
        f"- Rerun recommended from generated headline rows: `{any(str(row['rerun_recommended']).strip().lower() not in {'no', 'false', 'n/a', '', 'no_rerun_needed'} for row in aggregates['runs'])}`",
        "",
    ]
    if missing:
        lines.append("Runs with incomplete pack findings:")
        lines.extend(f"- `{row['run_label']}`" for row in missing)
    else:
        lines.append("No 10x rerun is recommended by this packaging audit. This is report packaging only; it did not rerun models.")
    return "\n".join(lines)


def risk_markdown(aggregates: dict[str, Any]) -> str:
    rows = [
        {
            "run_label": row["run_label"],
            "governed_rows": row["governed_rows"],
            "mock_tool_applied_rows": row["mock_tool_applied_rows"],
            "governed_risky_side_effect_completions": row["governed_risky_side_effect_completions"],
            "prompt_policy_leakage_rows": row["prompt_policy_leakage_rows"],
        }
        for row in aggregates["runs"]
    ]
    return "\n".join([
        "# Aegis 10 Run Risk Outcome Summary",
        "",
        "Aegis-governed risky side-effect completions are separate from prompt-policy leakage counterfactuals.",
        "",
        markdown_table(rows),
    ])


def provenance_markdown(aggregates: dict[str, Any]) -> str:
    rows = [
        {
            "run_label": row["run_label"],
            "trusted_aegis_resolved_provenance_rows": row["trusted_aegis_resolved_provenance_rows"],
            "provenance_unknown_rows": row["provenance_unknown_rows"],
            "provenance_invalid_rows": row["provenance_invalid_rows"],
        }
        for row in aggregates["runs"]
    ]
    return "\n".join([
        "# Aegis 10 Run Provenance Summary",
        "",
        "Evidence completeness is distinct from trusted Aegis-resolved provenance. Client/PEP-supplied citations are not accepted as production-valid policy evidence.",
        "",
        markdown_table(rows),
    ])


def zero_or_table(title: str, rows: list[dict[str, str]], predicate: Any, columns: list[str], empty: str) -> str:
    selected = [row for row in rows if predicate(row)]
    if not selected:
        return f"# {title}\n\n{empty}"
    return f"# {title}\n\n{markdown_table(selected, columns)}"


def grouped_markdown(title: str, rows: list[dict[str, str]], keys: list[str]) -> str:
    counts = Counter(tuple(row.get(key, "N/A") or "N/A" for key in keys) for row in rows)
    table = [
        {**{key: values[i] for i, key in enumerate(keys)}, "rows": count}
        for values, count in sorted(counts.items())
    ]
    return f"# {title}\n\n{markdown_table(table, [*keys, 'rows'])}"


def senate_latency_markdown(governed_rows: list[dict[str, str]]) -> str:
    by_run: dict[str, list[float]] = {}
    for row in governed_rows:
        value = as_float(row.get("senate_settlement_latency_ms"))
        if value is not None:
            by_run.setdefault(row.get("run_label", "N/A"), []).append(value)
    rows = []
    for run, values in sorted(by_run.items()):
        ordered = sorted(values)
        rows.append({
            "run_label": run,
            "rows": len(values),
            "min_ms": round(ordered[0], 3),
            "p50_ms": round(percentile(ordered, 50), 3),
            "mean_ms": round(mean(ordered), 3),
            "p90_ms": round(percentile(ordered, 90), 3),
            "p95_ms": round(percentile(ordered, 95), 3),
            "p99_ms": round(percentile(ordered, 99), 3),
            "max_ms": round(ordered[-1], 3),
        })
    if not rows:
        return "# Aegis 10 Run Senate Latency Summary\n\nN/A: no Senate settlement latency values were available."
    return "# Aegis 10 Run Senate Latency Summary\n\n" + markdown_table(rows)


def percentile(values: list[float], pct: float) -> float:
    if not values:
        return 0.0
    idx = min(len(values) - 1, max(0, round((pct / 100) * (len(values) - 1))))
    return values[idx]


def provenance_by_run_markdown(headline_rows: list[dict[str, str]]) -> str:
    rows = [
        {
            "run_label": row.get("run_label", "N/A"),
            "aegis_attempted_rows": row.get("aegis_attempted_rows", "N/A"),
            "provenance_boundary_valid_rows": row.get("provenance_boundary_valid_rows", "N/A"),
            "provenance_boundary_unknown_rows": row.get("provenance_boundary_unknown_rows", "N/A"),
            "provenance_boundary_invalid_rows": row.get("provenance_boundary_invalid_rows", "N/A"),
        }
        for row in headline_rows
    ]
    return "# Aegis 10 Run Provenance By Run\n\n" + markdown_table(rows)


def write_index() -> None:
    generated = sorted(path.name for path in OUT_DIR.iterdir() if path.is_file())
    lines = [
        "# 10 Run Comparison Report Index",
        "",
        "This directory is a Prompt G-style paper-facing pack for the completed 10x runs. It is generated from existing artifacts only.",
        "",
    ]
    lines.extend(f"- `{name}`" for name in generated)
    write_md(OUT_DIR / "REPORT_INDEX.md", "\n".join(lines))


def write_top_report(aggregates: dict[str, Any], completeness: list[dict[str, Any]]) -> None:
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
            "prompt_policy_leakage_rows": row["prompt_policy_leakage_rows"],
            "risk_completions": row["governed_risky_side_effect_completions"],
            "provenance_valid": row["trusted_aegis_resolved_provenance_rows"],
        }
        for row in aggregates["runs"]
    ]
    completeness_rows = [
        {
            "run_label": row["run_label"],
            "total_rows": row["actual_total_rows"],
            "governed_rows": row["actual_governed_rows"],
            "pack_complete": row["pack_complete"],
        }
        for row in completeness
    ]
    lines = [
        "# 10 Run Comparison Report",
        "",
        "## Executive Summary",
        "",
        f"- Included rows: `{aggregates['total_rows']}` total rows across five 10x packs.",
        f"- Governed rows: `{aggregates['governed_rows']}`.",
        f"- Aegis-attempted governed rows: `{aggregates['aegis_attempted_rows']}`.",
        f"- Governed risky side-effect completions: `{aggregates['governed_risky_side_effect_completions']}`.",
        f"- Governed mock tool applications: `{aggregates['mock_tool_applied_rows']}`.",
        f"- Senate queued rows: `{aggregates['senate_queued_rows']}`.",
        f"- Senate settled allowed rows: `{aggregates['senate_settled_allowed_rows']}`.",
        f"- Senate settled denied rows: `{aggregates['senate_settled_denied_rows']}`.",
        f"- Trusted Aegis-resolved provenance rows: `{aggregates['trusted_aegis_resolved_provenance_rows']}`.",
        f"- Prompt-policy leakage counterfactual rows: `{aggregates['prompt_policy_leakage_rows']}`.",
        f"- Overall pack complete: `{aggregates['overall_pack_complete']}`.",
        f"- Overall paper-ready verdict: `{aggregates['overall_paper_ready']}`.",
        "",
        "## Input Runs Included",
        "",
        markdown_table(completeness_rows),
        "",
        "## Headline Comparison",
        "",
        markdown_table(headline_rows),
        "",
        "## Governed Decision Comparison",
        "",
        "See `ten_run_report/AEGIS_10_RUN_HEADLINE.md`, `ten_run_report/AEGIS_10_RUN_GOVERNED_DECISION_TRACE.md`, and grouped bucket summaries.",
        "",
        "## Senate Settled Outcome Comparison",
        "",
        "Senate escalation means Senate voting path / execution withheld pending scoped signed tally where applicable. Settled Senate decisions are reported separately from the initial Aegis/PDP response.",
        "",
        "See `ten_run_report/AEGIS_10_RUN_SENATE_SUMMARY.md`, `ten_run_report/AEGIS_10_RUN_SENATE_BY_SETTLED_DECISION.md`, and `ten_run_report/AEGIS_10_RUN_SENATE_LATENCY_SUMMARY.md`.",
        "",
        "## Provenance Comparison",
        "",
        "Trusted provenance is counted only when generated on the Aegis/server side from verified policy/source controls. Client/PEP-supplied citations are not accepted as production-valid policy evidence.",
        "",
        "See `ten_run_report/AEGIS_10_RUN_PROVENANCE_SUMMARY.md` and `ten_run_report/AEGIS_10_RUN_PROVENANCE_BOUNDARY_AUDIT.md`.",
        "",
        "## Risk Outcome Comparison",
        "",
        "Aegis-governed risky side-effect completions are zero in this 10x pack. Prompt-policy leakage rows are listed separately with Aegis counterfactual decisions.",
        "",
        "See `ten_run_report/AEGIS_10_RUN_RISK_OUTCOME_SUMMARY.md`, `ten_run_report/PROMPT_POLICY_LEAKAGE_WITH_AEGIS_COUNTERFACTUAL.md`, and `ten_run_report/PROMPT_POLICY_LEAKAGE_EVENT_CHAIN.md`.",
        "",
        "## Tool, Control, Workflow, And Task Comparison",
        "",
        "See `ten_run_report/AEGIS_10_RUN_BY_TOOL_AND_BUCKET.md`, `ten_run_report/AEGIS_10_RUN_BY_CONTROL_AND_BUCKET.md`, `ten_run_report/AEGIS_10_RUN_BY_WORKFLOW_AND_BUCKET.md`, and `ten_run_report/AEGIS_10_RUN_BY_TASK.md`.",
        "",
        "## Rerun And Readiness Verdict",
        "",
        "This pack was generated from existing artifacts only. It did not rerun models, call Aegis/backend services, mutate policies, mutate prompts, or perform side effects.",
        "",
        "See `ten_run_report/AEGIS_10_RUN_PAPER_READINESS.md` and `ten_run_report/AEGIS_10_RUN_RERUN_READINESS_SUMMARY.md`.",
        "",
        "## Interpretation Notes",
        "",
        "- Raw Aegis decisions are preserved separately from normalized buckets.",
        "- Senate escalation means Senate voting path / execution withheld pending scoped signed tally where applicable.",
        "- A settled Senate `allow` does not mean the original mock tool was applied unless `mock_tool_applied=true`.",
        "- Evidence completeness is distinct from trusted Aegis-resolved provenance validity.",
        "- Client/PEP-supplied citations are not accepted as production-valid policy evidence.",
        "- Existing model outputs were not rerun by this report builder.",
    ]
    write_md(TOP_REPORT, "\n".join(lines))


if __name__ == "__main__":
    raise SystemExit(main())
