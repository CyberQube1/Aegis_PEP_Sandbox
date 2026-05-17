#!/usr/bin/env python3
"""Audit Aegis-attempted governed decisions for control provenance coverage.

This is an artifact-only QA helper: it reads matrix_records.jsonl files and does
not call models, Aegis, Civitas, or mock tools.
"""

from __future__ import annotations

import argparse
import json
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any


def _get(row: dict[str, Any], *path: str) -> Any:
    cur: Any = row
    for key in path:
        if not isinstance(cur, dict):
            return None
        cur = cur.get(key)
    return cur


def _as_list(value: Any) -> list[str]:
    if value is None:
        return []
    if isinstance(value, list):
        return [str(item).strip() for item in value if str(item).strip()]
    if isinstance(value, str):
        return [part.strip() for part in value.replace(",", ";").split(";") if part.strip()]
    return [str(value).strip()] if str(value).strip() else []


def _matrix_path(path: Path) -> Path:
    return path / "matrix_records.jsonl" if path.is_dir() else path


def load_rows(paths: list[Path]) -> list[tuple[Path, dict[str, Any]]]:
    rows: list[tuple[Path, dict[str, Any]]] = []
    for input_path in paths:
        path = _matrix_path(input_path)
        if not path.exists():
            raise SystemExit(f"missing matrix artifact: {path}")
        with path.open("r", encoding="utf-8") as handle:
            for line_number, line in enumerate(handle, 1):
                line = line.strip()
                if not line:
                    continue
                try:
                    rows.append((path, json.loads(line)))
                except json.JSONDecodeError as exc:
                    raise SystemExit(f"{path}:{line_number}: invalid json: {exc}") from exc
    return rows


def audit(paths: list[Path]) -> dict[str, Any]:
    per_control: dict[str, Counter[str]] = defaultdict(Counter)
    missing_rows: list[dict[str, Any]] = []
    status_counts: Counter[str] = Counter()
    attempted_rows = 0

    for path, row in load_rows(paths):
        if row.get("condition") != "aegis_governed_mesh_agent" or not row.get("aegis_decision_attempted"):
            continue
        attempted_rows += 1
        decision = row.get("aegis_decision") if isinstance(row.get("aegis_decision"), dict) else {}
        trace = decision.get("decision_trace") if isinstance(decision.get("decision_trace"), dict) else {}
        status = str(decision.get("provenance_status") or trace.get("provenance_status") or "unknown")
        status_counts[status] += 1
        controls = _as_list(decision.get("matched_control_ids") or trace.get("matched_control_ids") or decision.get("required_controls"))
        citations = decision.get("source_citations") or trace.get("source_citations") or []
        has_server_citation = bool(citations)
        for control_id in controls or ["N/A"]:
            per_control[control_id]["rows"] += 1
            per_control[control_id][status] += 1
            if has_server_citation:
                per_control[control_id]["rows_with_citations"] += 1
        if status != "complete":
            missing_rows.append(
                {
                    "artifact": str(path),
                    "task_id": row.get("task_id"),
                    "decision": decision.get("decision"),
                    "matched_control_ids": controls,
                    "required_controls": _as_list(decision.get("required_controls") or trace.get("required_controls")),
                    "provenance_status": status,
                    "provenance_status_reason": decision.get("provenance_status_reason")
                    or trace.get("provenance_status_reason"),
                    "reason_codes": _as_list(decision.get("reason_codes") or trace.get("reason_codes")),
                }
            )

    return {
        "input_paths": [str(_matrix_path(path)) for path in paths],
        "aegis_attempted_governed_rows": attempted_rows,
        "provenance_status_counts": dict(sorted(status_counts.items())),
        "controls": {
            control_id: dict(counter)
            for control_id, counter in sorted(per_control.items(), key=lambda item: item[0])
        },
        "missing_or_unknown_rows": missing_rows,
    }


def write_outputs(result: dict[str, Any], output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / "provenance_control_coverage_audit.json").write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    lines = [
        "# Provenance Control Coverage Audit",
        "",
        "Artifact-only audit. No model, Aegis, Civitas, backend, or mock-tool calls were made.",
        "",
        f"- Aegis-attempted governed rows: {result['aegis_attempted_governed_rows']}",
        f"- Provenance status counts: {result['provenance_status_counts']}",
        "",
        "## Controls",
        "",
        "| control_id | rows | rows_with_citations | complete | missing | unknown |",
        "|---|---:|---:|---:|---:|---:|",
    ]
    for control_id, counter in result["controls"].items():
        lines.append(
            "| {control_id} | {rows} | {rows_with_citations} | {complete} | {missing} | {unknown} |".format(
                control_id=control_id,
                rows=counter.get("rows", 0),
                rows_with_citations=counter.get("rows_with_citations", 0),
                complete=counter.get("complete", 0),
                missing=counter.get("missing", 0),
                unknown=counter.get("unknown", 0),
            )
        )
    lines.extend(["", "## Missing Or Unknown Rows", ""])
    if not result["missing_or_unknown_rows"]:
        lines.append("No Aegis-attempted governed rows with missing or unknown provenance were found.")
    else:
        lines.extend(
            [
                "| task_id | decision | provenance_status | matched_control_ids | reason |",
                "|---|---|---|---|---|",
            ]
        )
        for row in result["missing_or_unknown_rows"]:
            lines.append(
                "| {task_id} | {decision} | {status} | {controls} | {reason} |".format(
                    task_id=row.get("task_id") or "N/A",
                    decision=row.get("decision") or "N/A",
                    status=row.get("provenance_status") or "N/A",
                    controls="; ".join(row.get("matched_control_ids") or []) or "N/A",
                    reason=row.get("provenance_status_reason") or "N/A",
                )
            )
    (output_dir / "provenance_control_coverage_audit.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("inputs", nargs="+", type=Path, help="matrix_records.jsonl files or run output directories")
    parser.add_argument("--output-dir", type=Path, default=Path("reports"), help="directory for audit outputs")
    args = parser.parse_args()
    write_outputs(audit(args.inputs), args.output_dir)


if __name__ == "__main__":
    main()
