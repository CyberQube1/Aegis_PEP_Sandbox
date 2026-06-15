# Single Run Comparison Report

## Executive Summary

- Included rows: `630` total rows across five single-run packs.
- Governed rows: `210`.
- Aegis-attempted governed rows: `184`.
- Local fail-closed/no-tool rows: `26`.
- Initial execution-withheld rows: `182`.
- Senate queued rows: `102`.
- Senate settled allowed rows: `5`.
- Senate settled denied rows: `97`.
- Final signed tally rows: `102`.
- Quorum-met rows: `102`.
- Governed mock tool applications: `0`.
- Governed risky side-effect completions: `0`.
- Trusted Aegis-resolved provenance rows: `184`.
- Provenance unknown rows: `0`.
- Provenance invalid rows: `0`.
- Prompt-policy leakage counterfactual rows: `8`.
- Single-run pack complete: `True`.
- Any run needs rerun: `False`.
- Senate status joined where applicable: `True`.
- Single-run set ready for paper tables: `True`.

## Input Runs Included

| run_label | total_rows | governed_rows | pack_complete |
| --- | --- | --- | --- |
| stubbed_1x | 126 | 42 | True |
| gemma_1x | 126 | 42 | True |
| frontier_temp0_1x | 126 | 42 | True |
| frontier_temp07_1x | 126 | 42 | True |
| frontier_temp10_1x | 126 | 42 | True |

## Pack Completeness Status

See `single_run_report/AEGIS_SINGLE_RUN_PACK_COMPLETENESS.md`.

## Headline Comparison Table

| run_label | total_rows | governed_rows | aegis_attempted_rows | local_fail_closed_no_tool_rows | initial_execution_withheld_rows | senate_queued_rows | senate_settled_allowed_rows | senate_settled_denied_rows | mock_tool_applied_rows | risk_completions | trusted_provenance_rows |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| stubbed_1x | 126 | 42 | 42 | 0 | 40 | 40 | 5 | 35 | 0 | 0 | 42 |
| gemma_1x | 126 | 42 | 35 | 7 | 35 | 30 | 0 | 30 | 0 | 0 | 35 |
| frontier_temp0_1x | 126 | 42 | 37 | 5 | 37 | 12 | 0 | 12 | 0 | 0 | 37 |
| frontier_temp07_1x | 126 | 42 | 35 | 7 | 35 | 11 | 0 | 11 | 0 | 0 | 35 |
| frontier_temp10_1x | 126 | 42 | 35 | 7 | 35 | 9 | 0 | 9 | 0 | 0 | 35 |

## Governed Decision Comparison

See `single_run_report/AEGIS_SINGLE_RUN_GOVERNED_DECISION_TRACE.md`, `AEGIS_SINGLE_RUN_BY_DECISION_BUCKET.md`, and `AEGIS_SINGLE_RUN_PRACTICAL_EXECUTION_OUTCOMES.md`.

## Senate Settled Outcome Comparison

Senate escalation means Senate voting path. The report preserves initial Aegis/PDP response, queued state, async settled decision, finality, quorum, tally ID presence, and latency.

See `single_run_report/AEGIS_SINGLE_RUN_SENATE_SUMMARY.md` and `AEGIS_SINGLE_RUN_SENATE_LATENCY_SUMMARY.md`.

## Provenance Comparison

Evidence completeness is distinct from trusted Aegis-resolved provenance. Client/PEP-supplied citations are not counted as production-valid policy evidence.

See `single_run_report/AEGIS_SINGLE_RUN_PROVENANCE_SUMMARY.md` and `AEGIS_SINGLE_RUN_PROVENANCE_BOUNDARY_AUDIT.md`.

## Risk Outcome Comparison

A settled Senate `allow` does not mean the original mock tool was applied unless `mock_tool_applied=true`.

See `single_run_report/AEGIS_SINGLE_RUN_RISK_OUTCOME_SUMMARY.md`, `AEGIS_SINGLE_RUN_RISKY_COMPLETIONS.md`, `AEGIS_SINGLE_RUN_MOCK_TOOL_APPLICATIONS.md`, `PROMPT_POLICY_LEAKAGE_WITH_AEGIS_COUNTERFACTUAL.md`, and `PROMPT_POLICY_LEAKAGE_EVENT_CHAIN.md`.

## Tool/Control/Workflow Comparison

See `AEGIS_SINGLE_RUN_BY_TOOL_AND_BUCKET.md`, `AEGIS_SINGLE_RUN_BY_CONTROL_AND_BUCKET.md`, `AEGIS_SINGLE_RUN_BY_WORKFLOW_AND_BUCKET.md`, `AEGIS_SINGLE_RUN_BY_FAILURE_CATEGORY.md`, and `AEGIS_SINGLE_RUN_BY_TASK.md`.

## Expected-vs-Actual Summary

See `single_run_report/AEGIS_SINGLE_RUN_EXPECTED_VS_ACTUAL.md`.

## Rerun/Readiness Verdict

See `single_run_report/AEGIS_SINGLE_RUN_RERUN_READINESS_SUMMARY.md` and `AEGIS_SINGLE_RUN_PAPER_READINESS.md`.

## Interpretation Notes

- Raw Aegis decision, normalized decision bucket, practical execution outcome, and settled Senate decision are separate fields.
- Senate escalation means Senate voting path, not a generic manual-review path.
- Settled Senate allow is a governance settlement, not proof that the original mock tool was applied.
- Local fail-closed/no-tool rows where Aegis was not attempted are not counted as invalid provenance.
- This pack was generated from existing artifacts only. It did not rerun models, call Aegis/backend services, mutate policy, mutate prompts, or perform side effects.

## Detailed Tables

- `single_run_report/REPORT_INDEX.md`
- `single_run_report/AEGIS_SINGLE_RUN_HEADLINE.md`
- `single_run_report/AEGIS_SINGLE_RUN_GOVERNED_DECISION_TRACE.md`
- `single_run_report/AEGIS_SINGLE_RUN_SENATE_SUMMARY.md`
- `single_run_report/AEGIS_SINGLE_RUN_PROVENANCE_SUMMARY.md`
- `single_run_report/AEGIS_SINGLE_RUN_RISK_OUTCOME_SUMMARY.md`
- `single_run_report/AEGIS_SINGLE_RUN_PAPER_READINESS.md`
