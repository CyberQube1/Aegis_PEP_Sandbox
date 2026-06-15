# All One Run Comparison

This folder compares all completed 42-task single-pass runs.

## Runs

- `stubbed`: full 42-task x 3-condition stubbed run
- `gemma`: full 42-task x 3-condition Gemma run
- `frontier_temp0`: full 42-task x 3-condition Frontier run at temperature 0
- `frontier_temp07`: full 42-task x 3-condition Frontier run at temperature 0.7
- `frontier_temp10`: full 42-task x 3-condition Frontier run at temperature 1.0

## Contents

- `comparison_report/`: combined comparison report from the cleaned exporter
- `comparison_report/AEGIS_REJECTION_POLICY_TRACE.csv`: governed rejection/fail-closed trace table
- `comparison_report/AEGIS_REJECTION_POLICY_TRACE.md`: Markdown trace table
- `comparison_report/AEGIS_REJECTION_POLICY_TRACE.jsonl`: JSONL trace rows
- `source_outputs/`: copied raw one-run outputs

## Start Here

- `comparison_report/REPORT_INDEX.md`
- `comparison_report/HEADLINE_RESULTS_TABLE.md`
- `comparison_report/SHARED_TASK_COMPARISON.md`
- `comparison_report/AEGIS_REJECTION_POLICY_TRACE.md`
- `comparison_report/AEGIS_REJECTION_BY_DECISION.md`
- `comparison_report/PAPER_CLAIMS_AND_LIMITATIONS.md`
