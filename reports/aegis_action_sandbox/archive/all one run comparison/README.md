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
- `comparison_report/AEGIS_REJECTION_SOURCE_TRACE.csv`: expanded control/source citation trace
- `comparison_report/AEGIS_REJECTION_SOURCE_TRACE.md`: Markdown source trace table
- `comparison_report/AEGIS_REJECTION_SOURCE_TRACE.jsonl`: JSONL source trace rows
- `comparison_report/AEGIS_REJECTION_BY_SOURCE_DOCUMENT.md`: grouped rejection counts by source document
- `comparison_report/AEGIS_REJECTION_BY_SOURCE_SECTION.md`: grouped rejection counts by indexed source section/page
- `comparison_report/AEGIS_REJECTION_BY_CONTROL_AND_SOURCE.md`: grouped control/source provenance
- `comparison_report/AEGIS_REJECTION_SOURCE_DEREFERENCE_STATUS.md`: source dereference completeness/status counts
- `comparison_report/AEGIS_GOVERNED_DECISION_TRACE.csv`: full governed decision trace over every governed row
- `comparison_report/AEGIS_GOVERNED_DECISION_HEADLINE.md`: headline governed decision/rerun table
- `comparison_report/AEGIS_ARTIFACT_AUDIT.md`: artifact completeness and rerun-readiness audit
- `comparison_report/AEGIS_PROVENANCE_BOUNDARY_AUDIT.md`: trusted Aegis provenance boundary audit
- `source_outputs/`: copied raw one-run outputs

## What Changed

- Rejection traces now join task-level controls/source refs with Praxis source manifests and local per-org/per-baseline chunk indexes.
- Source trace rows include source title, type, regulator/owner, indexed section/page, MinIO/S3 object path, dereference status, and excerpt/rationale fields where available.
- Missing source excerpts or exact section metadata are emitted as `N/A` with an explicit `source_dereference_status`; the report does not invent citation text.
- Full governed decision reports now summarize allowed/approved, blocked, Senate escalation, execution-withheld, local fail-closed/no-action, parser/backend failure, and unknown buckets.
- Artifact and provenance-boundary audits distinguish evidence completeness from trusted Aegis-resolved provenance validity. Client/PEP-supplied citations are not accepted as production-valid policy evidence.
- This comparison script regenerates reports from existing one-run artifacts only. It does not run models, call Aegis/backend services, mutate prompts/policies/tasks, or apply tools.

## Start Here

- `comparison_report/REPORT_INDEX.md`
- `comparison_report/HEADLINE_RESULTS_TABLE.md`
- `comparison_report/SHARED_TASK_COMPARISON.md`
- `comparison_report/AEGIS_REJECTION_POLICY_TRACE.md`
- `comparison_report/AEGIS_REJECTION_SOURCE_TRACE.md`
- `comparison_report/AEGIS_REJECTION_BY_SOURCE_DOCUMENT.md`
- `comparison_report/AEGIS_REJECTION_SOURCE_DEREFERENCE_STATUS.md`
- `comparison_report/AEGIS_REJECTION_BY_DECISION.md`
- `comparison_report/AEGIS_GOVERNED_DECISION_HEADLINE.md`
- `comparison_report/AEGIS_ARTIFACT_AUDIT.md`
- `comparison_report/AEGIS_PROVENANCE_BOUNDARY_AUDIT.md`
- `comparison_report/PAPER_CLAIMS_AND_LIMITATIONS.md`
