# Frontier One Run

This folder contains the clean Frontier full 1x paper pack.

## Contents

- `frontier_output/`: raw Frontier full 1x output copied from `outputs_island/frontier_full_1x_20260514T022554Z`
- `frontier_output/senate_async_status_snapshot.jsonl`: settled Senate voting path status snapshot collected after the matrix run
- `frontier_report/`: regenerated Frontier-only report using the cleaned exporter
- `frontier_report/AEGIS_SENATE_SETTLED_ALLOWED_ACTIONS.md`: settled Senate-allowed governed actions
- `frontier_report/AEGIS_SENATE_SETTLED_DENIED_ACTIONS.md`: settled Senate-denied governed actions
- `frontier_report/tables/`: CSV and Markdown table fragments
- `frontier_report/latex/`: LaTeX table fragments
- `frontier_report/figures/data/`: figure-ready CSVs

## Start Here

- `frontier_report/REPORT_INDEX.md`
- `frontier_report/AEGIS_GOVERNED_DECISION_HEADLINE.md`
- `frontier_report/AEGIS_SENATE_ASYNC_STATUS_SUMMARY.md`
- `frontier_report/HEADLINE_RESULTS_TABLE.md`
- `frontier_report/PAPER_CLAIMS_AND_LIMITATIONS.md`
- `frontier_report/normalized_results.csv`
- `frontier_output/matrix_records.jsonl`

No Gemma or Stubbed comparison runs are included in this folder.

The initial PDP rows may show Senate escalation as pending because Aegis returns before async voting completes. The settled Senate verdicts are captured in `senate_async_status_snapshot.jsonl` and included in the generated report.
