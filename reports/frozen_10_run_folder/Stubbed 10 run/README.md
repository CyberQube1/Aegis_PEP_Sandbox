# Stubbed 10 Run

This folder contains the clean Stubbed 10x paper pack.

## Contents

- `stubbed_output/`: raw Stubbed 10x output copied from `outputs_island/paper_matrix_stubbed_10x_20260514T015933Z`
- `stubbed_output/senate_async_status_snapshot.jsonl`: settled Senate voting path status snapshot collected after the matrix run
- `stubbed_report/`: regenerated Stubbed 10x report using the cleaned exporter and Senate snapshot
- `STUBBED_10_RUN_REPORT.md`: concise top-level report

## Start Here

- `STUBBED_10_RUN_REPORT.md`
- `stubbed_report/REPORT_INDEX.md`
- `stubbed_report/AEGIS_GOVERNED_DECISION_HEADLINE.md`
- `stubbed_report/AEGIS_SENATE_ASYNC_STATUS_SUMMARY.md`
- `stubbed_report/AEGIS_SENATE_SETTLED_ALLOWED_ACTIONS.md`
- `stubbed_report/AEGIS_SENATE_SETTLED_DENIED_ACTIONS.md`
- `stubbed_output/senate_async_status_summary.json`
- `stubbed_output/loop_*/matrix_records.jsonl`

The initial PDP rows may show Senate escalation as pending because Aegis returns before async voting completes. The settled Senate verdicts are captured in `senate_async_status_snapshot.jsonl` and included in the generated report.
