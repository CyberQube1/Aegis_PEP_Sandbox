# Frontier Temp 0.7 10 Run

This folder contains the clean Frontier temp 0.7 10x paper pack.

## Contents

- `frontier_output/`: raw Frontier 10x output copied from `outputs_island/paper_matrix_frontier_temp_0.7_10x_20260514T033039Z`
- `frontier_output/senate_async_status_snapshot.jsonl`: settled Senate voting path status snapshot collected after the matrix run
- `frontier_report/`: regenerated Frontier 10x report using the cleaned exporter and Senate snapshot
- `FRONTIER_TEMP_0.7_10_RUN_REPORT.md`: concise top-level report

## Start Here

- `FRONTIER_TEMP_0.7_10_RUN_REPORT.md`
- `frontier_report/REPORT_INDEX.md`
- `frontier_report/AEGIS_GOVERNED_DECISION_HEADLINE.md`
- `frontier_report/AEGIS_SENATE_ASYNC_STATUS_SUMMARY.md`
- `frontier_report/AEGIS_SENATE_SETTLED_ALLOWED_ACTIONS.md`
- `frontier_report/AEGIS_SENATE_SETTLED_DENIED_ACTIONS.md`
- `frontier_output/senate_async_status_summary.json`
- `frontier_output/loop_*/matrix_records.jsonl`

The initial PDP rows may show Senate escalation as pending because Aegis returns before async voting completes. The settled Senate verdicts are captured in `senate_async_status_snapshot.jsonl` and included in the generated report.
