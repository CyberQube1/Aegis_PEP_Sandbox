from __future__ import annotations

from collections import Counter, defaultdict
from statistics import mean, median
from typing import Any, Iterable

from harness.reports.normalize_results import as_float


def summarize_rows(rows: list[dict[str, Any]]) -> dict[str, Any]:
    total = len(rows)
    governed = [row for row in rows if row.get("condition") == "aegis_governed_mesh_agent"]
    aegis_latencies = numbers(row.get("aegis_decision_ms") for row in rows)
    model_latencies = numbers(row.get("latency_model_ms") for row in rows)
    total_latencies = numbers(row.get("latency_total_ms") for row in rows)
    return {
        "total_rows": total,
        "unique_tasks": len({row.get("task_id") for row in rows if row.get("task_id") not in {None, "N/A", ""}}),
        "rows_by_condition": dict(Counter(row.get("condition", "N/A") for row in rows)),
        "rows_by_model": dict(Counter(row.get("paper_model_label", "N/A") for row in rows)),
        "infrastructure_failures": count_where(rows, lambda row: row.get("infrastructure_status") != "ok"),
        "parser_success_rows": count_where(rows, lambda row: row.get("parser_status") in {"parsed_json", "parsed", "ok"}),
        "model_generated_action_rows": count_where(rows, lambda row: bool(row.get("model_generated_action"))),
        "fallback_or_heuristic_rows": count_where(rows, lambda row: bool(row.get("fallback_or_heuristic"))),
        "model_backend_failures": count_where(rows, lambda row: bool(row.get("model_backend_failure"))),
        "governed_rows": len(governed),
        "aegis_attempted_rows": count_where(rows, lambda row: bool(row.get("aegis_decision_attempted"))),
        "aegis_latency": latency_stats(aegis_latencies),
        "model_latency": latency_stats(model_latencies),
        "total_latency": latency_stats(total_latencies),
        "evidence_complete_rows": count_where(rows, lambda row: bool(row.get("evidence_complete"))),
        "mock_tool_applied_rows": count_where(rows, lambda row: bool(row.get("mock_tool_applied"))),
        "risky_action_flagged_rows": count_where(rows, lambda row: bool(row.get("risky_action_flagged"))),
        "risky_action_completed_rows": count_where(rows, lambda row: bool(row.get("risky_action_completed"))),
        "blocked_or_review_rows": count_where(rows, lambda row: bool(row.get("blocked_or_review"))),
        "governed_risky_side_effects_completed": count_where(
            rows,
            lambda row: row.get("condition") == "aegis_governed_mesh_agent"
            and bool(row.get("risky_action_completed")),
        ),
        "no_tool_fail_closed_rows": count_where(rows, infer_no_tool_fail_closed),
        "rows_by_failure_category": dict(Counter(row.get("failure_category", "N/A") for row in rows)),
        "rows_by_workflow_family": dict(Counter(row.get("workflow_family", "N/A") for row in rows)),
    }


def summarize_by(rows: list[dict[str, Any]], keys: list[str]) -> list[dict[str, Any]]:
    grouped: dict[tuple[Any, ...], list[dict[str, Any]]] = defaultdict(list)
    for row in rows:
        grouped[tuple(row.get(key, "N/A") for key in keys)].append(row)

    output: list[dict[str, Any]] = []
    for group_key, items in sorted(grouped.items(), key=lambda item: tuple(str(part) for part in item[0])):
        summary = summarize_rows(items)
        record = {key: group_key[index] for index, key in enumerate(keys)}
        record.update(flatten_summary(summary))
        output.append(record)
    return output


def flatten_summary(summary: dict[str, Any]) -> dict[str, Any]:
    total = max(int(summary["total_rows"]), 1)
    return {
        "rows": summary["total_rows"],
        "unique_tasks": summary["unique_tasks"],
        "infrastructure_failures": summary["infrastructure_failures"],
        "parser_success_rows": summary["parser_success_rows"],
        "parser_success_rate": rate(summary["parser_success_rows"], total),
        "model_generated_action_rows": summary["model_generated_action_rows"],
        "fallback_or_heuristic_rows": summary["fallback_or_heuristic_rows"],
        "model_backend_failures": summary["model_backend_failures"],
        "governed_rows": summary["governed_rows"],
        "aegis_attempted_rows": summary["aegis_attempted_rows"],
        "aegis_avg_ms": summary["aegis_latency"]["avg_ms"],
        "aegis_median_ms": summary["aegis_latency"]["median_ms"],
        "aegis_p95_ms": summary["aegis_latency"]["p95_ms"],
        "aegis_max_ms": summary["aegis_latency"]["max_ms"],
        "model_avg_ms": summary["model_latency"]["avg_ms"],
        "model_median_ms": summary["model_latency"]["median_ms"],
        "model_p95_ms": summary["model_latency"]["p95_ms"],
        "model_max_ms": summary["model_latency"]["max_ms"],
        "total_avg_ms": summary["total_latency"]["avg_ms"],
        "total_median_ms": summary["total_latency"]["median_ms"],
        "total_p95_ms": summary["total_latency"]["p95_ms"],
        "total_max_ms": summary["total_latency"]["max_ms"],
        "evidence_complete_rows": summary["evidence_complete_rows"],
        "evidence_complete_rate": rate(summary["evidence_complete_rows"], total),
        "mock_tool_applied_rows": summary["mock_tool_applied_rows"],
        "mock_tool_applied_rate": rate(summary["mock_tool_applied_rows"], total),
        "risky_action_flagged_rows": summary["risky_action_flagged_rows"],
        "risky_action_completed_rows": summary["risky_action_completed_rows"],
        "risky_action_completed_rate": rate(
            summary["risky_action_completed_rows"], max(summary["risky_action_flagged_rows"], 1)
        ),
        "risky_completed_per_risky_flagged": rate(
            summary["risky_action_completed_rows"], max(summary["risky_action_flagged_rows"], 1)
        ),
        "risky_completed_per_all_rows": rate(summary["risky_action_completed_rows"], total),
        "blocked_or_review_rows": summary["blocked_or_review_rows"],
        "governed_risky_side_effects_completed": summary["governed_risky_side_effects_completed"],
        "no_tool_fail_closed_rows": summary["no_tool_fail_closed_rows"],
    }


def latency_stats(values: list[float]) -> dict[str, float | None]:
    if not values:
        return {"avg_ms": None, "median_ms": None, "p95_ms": None, "max_ms": None}
    sorted_values = sorted(values)
    return {
        "avg_ms": round(mean(sorted_values), 3),
        "median_ms": round(median(sorted_values), 3),
        "p95_ms": round(percentile(sorted_values, 95), 3),
        "max_ms": round(max(sorted_values), 3),
    }


def percentile(sorted_values: list[float], percentile_value: float) -> float:
    if not sorted_values:
        raise ValueError("percentile requires at least one value")
    if len(sorted_values) == 1:
        return sorted_values[0]
    rank = (percentile_value / 100) * (len(sorted_values) - 1)
    lower = int(rank)
    upper = min(lower + 1, len(sorted_values) - 1)
    fraction = rank - lower
    return sorted_values[lower] + ((sorted_values[upper] - sorted_values[lower]) * fraction)


def numbers(values: Iterable[Any]) -> list[float]:
    output: list[float] = []
    for value in values:
        number = as_float(value)
        if number is not None:
            output.append(number)
    return output


def count_where(rows: list[dict[str, Any]], predicate) -> int:
    return sum(1 for row in rows if predicate(row))


def rate(numerator: int, denominator: int) -> float:
    if denominator == 0:
        return 0.0
    return round(numerator / denominator, 4)


def infer_no_tool_fail_closed(row: dict[str, Any]) -> bool:
    if row.get("final_decision") != "fail_closed_no_action":
        return False
    if row.get("aegis_decision_attempted"):
        return False
    proposed_tool = str(row.get("proposed_tool") or "").strip()
    reason = str(row.get("proposal_failure_reason") or "").lower()
    return proposed_tool in {"", "N/A", "none", "null"} or "no tool" in reason or "no-side-effect" in reason
