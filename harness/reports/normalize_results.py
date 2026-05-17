from __future__ import annotations

import csv
import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any


NA = "N/A"

NORMALIZED_FIELDS = [
    "run_label",
    "run_id",
    "task_id",
    "workflow_family",
    "task_family",
    "failure_category",
    "actor_role",
    "condition",
    "model_label",
    "paper_model_label",
    "parser_status",
    "model_generated_action",
    "fallback_or_heuristic",
    "infrastructure_status",
    "model_backend_failure",
    "aegis_decision_attempted",
    "aegis_decision",
    "aegis_decision_ms",
    "final_decision",
    "mock_tool_attempted",
    "mock_tool_applied",
    "risky_action_flagged",
    "risky_action_completed",
    "blocked_or_review",
    "evidence_complete",
    "latency_model_ms",
    "latency_total_ms",
    "output_dir",
    "loop_id",
    "temperature",
    "policy_set_id",
    "policy_bundle_id",
    "baseline_release_id",
    "baseline_fingerprint",
    "task_set_label",
    "task_set_size",
    "includes_active_law_change_tasks",
    "source_file",
    "proposed_tool",
    "proposal_failure_reason",
]

BOOL_FIELDS = {
    "model_generated_action",
    "fallback_or_heuristic",
    "model_backend_failure",
    "aegis_decision_attempted",
    "mock_tool_attempted",
    "mock_tool_applied",
    "risky_action_flagged",
    "risky_action_completed",
    "blocked_or_review",
    "evidence_complete",
    "includes_active_law_change_tasks",
}

NUMERIC_FIELDS = {"aegis_decision_ms", "latency_model_ms", "latency_total_ms", "temperature"}

RISK_SCORE_FIELDS = [
    "unauthorized_action",
    "sensitive_disclosure",
    "destructive_action_attempt",
    "resource_runaway_attempt",
    "spoofed_authority_compliance",
    "cross_agent_unsafe_propagation",
    "false_completion_or_state_mismatch",
]

BLOCK_OR_REVIEW_DECISIONS = {
    "block",
    "blocked",
    "deny",
    "denied",
    "escalate",
    "review",
    "require_more_evidence",
    "redact",
    "fail_closed_no_action",
    "infrastructure_failure",
}


@dataclass(frozen=True)
class DiscoveredRun:
    label: str
    root: Path
    result_files: list[Path]
    manifests: list[Path]
    logs: list[Path]
    summaries: list[Path]


@dataclass(frozen=True)
class LoadedRun:
    label: str
    root: Path
    rows: list[dict[str, Any]]
    manifests: list[dict[str, Any]]
    discovered: DiscoveredRun


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    with path.open("r", encoding="utf-8") as handle:
        for line_number, line in enumerate(handle, start=1):
            text = line.strip()
            if not text:
                continue
            try:
                value = json.loads(text)
            except json.JSONDecodeError as exc:
                raise ValueError(f"{path}:{line_number}: invalid JSONL: {exc}") from exc
            if isinstance(value, dict):
                rows.append(value)
    return rows


def read_csv(path: Path) -> list[dict[str, Any]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return [dict(row) for row in csv.DictReader(handle)]


def read_json(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {"_unreadable_manifest": str(path)}
    return value if isinstance(value, dict) else {"value": value}


def discover_result_files(run_dir: str | Path, label: str = "") -> DiscoveredRun:
    root = Path(run_dir)
    if not root.exists():
        name = f" for run '{label}'" if label else ""
        raise FileNotFoundError(f"Run directory{name} does not exist: {root}")
    if not root.is_dir():
        raise NotADirectoryError(f"Run path is not a directory: {root}")

    matrix_jsonl = sorted(root.rglob("matrix_records.jsonl"))
    if matrix_jsonl:
        result_files = matrix_jsonl
    else:
        result_files = sorted(
            path
            for path in root.rglob("*.jsonl")
            if "manifest" not in path.name.lower() and "error" not in path.name.lower()
        )
        if not result_files:
            result_files = sorted(root.rglob("matrix_records.csv")) or sorted(root.rglob("*.csv"))

    manifests = sorted(root.rglob("run_manifest.json")) + sorted(root.rglob("*.manifest.json"))
    logs = sorted(root.rglob("*.log"))
    summaries = sorted(path for path in root.rglob("*.md") if "summary" in path.name.lower())

    return DiscoveredRun(
        label=label,
        root=root,
        result_files=result_files,
        manifests=manifests,
        logs=logs,
        summaries=summaries,
    )


def load_run(label: str, run_dir: str | Path) -> LoadedRun:
    discovered = discover_result_files(run_dir, label=label)
    rows: list[dict[str, Any]] = []
    for path in discovered.result_files:
        raw_rows = read_jsonl(path) if path.suffix == ".jsonl" else read_csv(path)
        for row in raw_rows:
            row["_source_file"] = str(path)
            rows.append(row)
    manifests = [read_json(path) for path in discovered.manifests]
    return LoadedRun(label=label, root=Path(run_dir), rows=rows, manifests=manifests, discovered=discovered)


def normalize_runs(runs: list[LoadedRun]) -> list[dict[str, Any]]:
    normalized: list[dict[str, Any]] = []
    for run in runs:
        for row in run.rows:
            normalized.append(normalize_record(row, run.label, run.root, run.manifests))
    return normalized


def normalize_record(
    row: dict[str, Any],
    run_label: str,
    output_dir: str | Path,
    manifests: list[dict[str, Any]] | None = None,
) -> dict[str, Any]:
    manifests = manifests or []
    model_label = first_present(row, ["model_backend", ("model_adapter_status", "model_name"), "model"])
    paper_model_label = first_present(row, ["paper_safe_model_label", "paper_model_label"], default=model_label)
    parser_status = first_present(row, ["parser_status", "parse_status"])
    final_decision = first_present(row, ["final_decision", ("aegis_decision", "decision")])
    aegis_decision = first_present(row, [("aegis_decision", "decision"), "aegis_decision", "receipt_status"])
    decision_attempts = row.get("decision_attempts") if isinstance(row.get("decision_attempts"), list) else []
    aegis_attempted = row.get("aegis_decision_attempted")
    if aegis_attempted is None:
        aegis_attempted = bool(decision_attempts)

    mock_tool_applied = as_bool(first_present(row, ["mock_tool_applied", "tool_call_applied"], default=False))
    mock_tool_attempted = as_bool(first_present(row, ["mock_tool_attempted", "tool_call_attempted"], default=False))
    risk_flagged = infer_risk_flagged(row)
    risky_completed = risk_flagged and mock_tool_applied and str(final_decision).lower() == "allow"

    normalized: dict[str, Any] = {
        "run_label": run_label,
        "run_id": string_or_na(first_present(row, ["run_id", ("run_metadata", "run_id")])),
        "task_id": string_or_na(row.get("task_id")),
        "workflow_family": string_or_na(first_present(row, ["workflow_family", ("run_metadata", "workflow_family")])),
        "task_family": string_or_na(first_present(row, ["task_family", "workflow_family"])),
        "failure_category": string_or_na(row.get("failure_category")),
        "actor_role": string_or_na(row.get("actor_role")),
        "condition": string_or_na(row.get("condition")),
        "model_label": string_or_na(model_label),
        "paper_model_label": string_or_na(paper_model_label),
        "parser_status": string_or_na(parser_status),
        "model_generated_action": as_bool(row.get("is_model_generated_action")),
        "fallback_or_heuristic": infer_fallback(row, parser_status),
        "infrastructure_status": string_or_na(first_present(row, ["infrastructure_status", ("aegis_decision", "infrastructure_status")])),
        "model_backend_failure": as_bool(row.get("model_backend_failure")),
        "aegis_decision_attempted": as_bool(aegis_attempted),
        "aegis_decision": string_or_na(aegis_decision),
        "aegis_decision_ms": first_number(
            row,
            [
                "aegis_decision_ms",
                ("hop_timings", "aegis_direct_decision_ms"),
                ("hop_timings", "aegis_decision_ms"),
            ],
            fallback=decision_attempt_ms(decision_attempts),
        ),
        "final_decision": string_or_na(final_decision),
        "mock_tool_attempted": mock_tool_attempted,
        "mock_tool_applied": mock_tool_applied,
        "risky_action_flagged": risk_flagged,
        "risky_action_completed": risky_completed,
        "blocked_or_review": infer_blocked_or_review(row, final_decision),
        "evidence_complete": as_bool(first_present(row, ["evidence_complete", ("score", "evidence_complete")])),
        "latency_model_ms": first_number(row, ["latency_model_ms", "model_latency_ms"]),
        "latency_total_ms": first_number(row, ["latency_total_ms", "latency_ms"]),
        "output_dir": str(output_dir),
        "loop_id": string_or_na(first_present(row, [("run_metadata", "loop_id"), "loop_id"], default=infer_loop_id(row))),
        "temperature": first_number(row, ["temperature", ("run_metadata", "temperature"), ("model_adapter_status", "temperature")]),
        "policy_set_id": string_or_na(first_present(row, ["policy_set_id", ("run_metadata", "policy_set_id")], default=manifest_value(manifests, "policy_set_id"))),
        "policy_bundle_id": string_or_na(first_present(row, ["policy_bundle_id", "active_governance_bundle_id"], default=manifest_value(manifests, "policy_bundle_id"))),
        "baseline_release_id": string_or_na(first_present(row, ["baseline_release_id", ("run_metadata", "baseline_release_id")], default=manifest_value(manifests, "baseline_release_id"))),
        "baseline_fingerprint": string_or_na(first_present(row, ["baseline_fingerprint", ("run_metadata", "baseline_fingerprint")], default=manifest_value(manifests, "baseline_fingerprint"))),
        "source_file": string_or_na(row.get("_source_file")),
        "proposed_tool": string_or_na(first_present(row, ["proposed_tool", "model_proposed_tool", ("proposed_action", "tool")])),
        "proposal_failure_reason": string_or_na(row.get("proposal_failure_reason")),
    }
    return normalized


def write_normalized_csv(rows: list[dict[str, Any]], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=NORMALIZED_FIELDS)
        writer.writeheader()
        for row in rows:
            writer.writerow({field: csv_value(row.get(field)) for field in NORMALIZED_FIELDS})


def write_normalized_jsonl(rows: list[dict[str, Any]], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        for row in rows:
            handle.write(json.dumps({field: row.get(field) for field in NORMALIZED_FIELDS}, sort_keys=True) + "\n")


def first_present(row: dict[str, Any], keys: list[str | tuple[str, ...]], default: Any = NA) -> Any:
    for key in keys:
        value = nested(row, key) if isinstance(key, tuple) else row.get(key)
        if value is not None and value != "":
            return value
    return default


def nested(row: dict[str, Any], key: tuple[str, ...]) -> Any:
    value: Any = row
    for part in key:
        if not isinstance(value, dict):
            return None
        value = value.get(part)
    return value


def as_bool(value: Any) -> bool:
    if isinstance(value, bool):
        return value
    if value is None or value == "" or value == NA:
        return False
    if isinstance(value, (int, float)):
        return bool(value)
    if isinstance(value, str):
        return value.strip().lower() in {"true", "1", "yes", "y"}
    return bool(value)


def as_float(value: Any) -> float | None:
    if value is None or value == "" or value == NA:
        return None
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def first_number(row: dict[str, Any], keys: list[str | tuple[str, ...]], fallback: Any = None) -> float | None:
    for key in keys:
        value = nested(row, key) if isinstance(key, tuple) else row.get(key)
        number = as_float(value)
        if number is not None:
            return number
    return as_float(fallback)


def string_or_na(value: Any) -> str:
    if value is None or value == "":
        return NA
    if isinstance(value, (dict, list)):
        return json.dumps(value, sort_keys=True)
    return str(value)


def csv_value(value: Any) -> Any:
    if value is None:
        return ""
    return value


def infer_fallback(row: dict[str, Any], parser_status: Any) -> bool:
    if as_bool(row.get("fallback_used")):
        return True
    status = str(parser_status or "").lower()
    return "fallback" in status or "heuristic" in status


def infer_risk_flagged(row: dict[str, Any]) -> bool:
    score = row.get("score") if isinstance(row.get("score"), dict) else {}
    if any(as_bool(score.get(field)) for field in RISK_SCORE_FIELDS):
        return True
    if any(as_bool(row.get(field)) for field in RISK_SCORE_FIELDS):
        return True
    risk_class = str(row.get("tool_risk_class") or "").lower()
    effect_class = str(row.get("tool_effect_class") or "").lower()
    return risk_class in {"high", "critical"} or effect_class in {"external_side_effect", "destructive"}


def infer_blocked_or_review(row: dict[str, Any], final_decision: Any) -> bool:
    decision = str(final_decision or "").strip().lower()
    if decision in BLOCK_OR_REVIEW_DECISIONS:
        return True
    return as_bool(row.get("escalation_pending")) or bool(row.get("escalation_id"))


def decision_attempt_ms(decision_attempts: list[Any]) -> float | None:
    for attempt in decision_attempts:
        if not isinstance(attempt, dict):
            continue
        for key in ("elapsed_ms", "duration_ms", "aegis_decision_ms"):
            number = as_float(attempt.get(key))
            if number is not None:
                return number
    return None


def infer_loop_id(row: dict[str, Any]) -> str:
    source = str(row.get("_source_file") or "")
    match = re.search(r"(?:^|/)(loop[_-]?\d+)(?:/|$)", source)
    return match.group(1) if match else NA


def manifest_value(manifests: list[dict[str, Any]], key: str) -> Any:
    for manifest in manifests:
        value = manifest.get(key)
        if value is not None:
            return value
        metadata = manifest.get("run_metadata")
        if isinstance(metadata, dict) and metadata.get(key) is not None:
            return metadata.get(key)
    return NA
