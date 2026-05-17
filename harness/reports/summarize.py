from __future__ import annotations

import argparse
from collections import defaultdict
from pathlib import Path

from harness.utils.io import read_jsonl


def _collect_rows(path: str) -> list[dict]:
    source = Path(path)
    if source.is_dir():
        rows: list[dict] = []
        for candidate in sorted(source.glob("*.jsonl")):
            rows.extend(read_jsonl(candidate))
        return rows
    return read_jsonl(source)


def summarize(input_path: str, output_path: str) -> None:
    rows = _collect_rows(input_path)
    grouped: dict[tuple[str, str, str, str], list[dict]] = defaultdict(list)
    for row in rows:
        grouped[
            (
                str(row.get("condition")),
                str(row.get("paper_safe_model_label")),
                str(row.get("workflow_family")),
                str(row.get("failure_category")),
            )
        ].append(row)

    lines = [
        "# Sandbox Summary",
        "",
        "| Condition | Model | Workflow family | Failure category | Runs | Success | Infra failures | Unauthorized action | Correct block/escalation | Sensitive disclosure | Destructive action attempt | Resource runaway attempt | Authority spoofing compliance | Cross-agent unsafe propagation | False completion/state mismatch | Evidence complete | Mock tool applied |",
        "| --- | --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |",
    ]
    for (condition, model_label, workflow_family, failure_category), items in sorted(grouped.items()):
        success = sum(1 for item in items if item.get("final_decision") != "infrastructure_failure")
        infra_failures = sum(1 for item in items if item.get("final_decision") == "infrastructure_failure")
        unauthorized = sum(1 for item in items if item.get("score", {}).get("unauthorized_action"))
        correct = sum(1 for item in items if item.get("score", {}).get("correct_block_or_escalation"))
        sensitive = sum(1 for item in items if item.get("score", {}).get("sensitive_disclosure"))
        destructive = sum(1 for item in items if item.get("score", {}).get("destructive_action_attempt"))
        runaway = sum(1 for item in items if item.get("score", {}).get("resource_runaway_attempt"))
        spoofed = sum(1 for item in items if item.get("score", {}).get("spoofed_authority_compliance"))
        propagation = sum(1 for item in items if item.get("score", {}).get("cross_agent_unsafe_propagation"))
        false_completion = sum(1 for item in items if item.get("score", {}).get("false_completion_or_state_mismatch"))
        evidence = sum(1 for item in items if item.get("score", {}).get("evidence_complete"))
        applied = sum(1 for item in items if item.get("mock_tool_applied"))
        lines.append(
            f"| {condition} | {model_label} | {workflow_family} | {failure_category} | {len(items)} | {success} | {infra_failures} | {unauthorized} | {correct} | {sensitive} | {destructive} | {runaway} | {spoofed} | {propagation} | {false_completion} | {evidence} | {applied} |"
        )
    target = Path(output_path)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Summarize sandbox JSONL outputs")
    parser.add_argument("--input", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args(argv)
    summarize(args.input, args.output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
