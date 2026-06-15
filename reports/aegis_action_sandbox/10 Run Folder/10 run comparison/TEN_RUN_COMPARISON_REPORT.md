# 10 Run Comparison Report

## Executive Summary

- Included rows: `6300` total rows across five 10x packs.
- Governed rows: `2100`.
- Aegis-attempted governed rows: `1832`.
- Governed risky side-effect completions: `0`.
- Governed mock tool applications: `0`.
- Senate queued rows: `1019`.
- Senate settled allowed rows: `60`.
- Senate settled denied rows: `959`.
- Trusted Aegis-resolved provenance rows: `1832`.
- Prompt-policy leakage counterfactual rows: `79`.
- Overall pack complete: `True`.
- Overall paper-ready verdict: `True`.

## Input Runs Included

| run_label | total_rows | governed_rows | pack_complete |
| --- | --- | --- | --- |
| stubbed_10_run | 1260 | 420 | True |
| gemma_10_run | 1260 | 420 | True |
| frontier_temp_0_10_run | 1260 | 420 | True |
| frontier_temp_0.7_10_run | 1260 | 420 | True |
| frontier_temp_1.0_10_run | 1260 | 420 | True |

## Headline Comparison

| run_label | total_rows | governed_rows | aegis_attempted_rows | local_fail_closed_no_tool_rows | initial_execution_withheld_rows | senate_queued_rows | senate_settled_allowed_rows | senate_settled_denied_rows | prompt_policy_leakage_rows | risk_completions | provenance_valid |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| stubbed_10_run | 1260 | 420 | 420 | 0 | 400 | 400 | 50 | 350 | 20 | 0 | 420 |
| gemma_10_run | 1260 | 420 | 350 | 70 | 350 | 300 | 10 | 290 | 0 | 0 | 350 |
| frontier_temp_0_10_run | 1260 | 420 | 367 | 53 | 367 | 119 | 0 | 119 | 20 | 0 | 367 |
| frontier_temp_0.7_10_run | 1260 | 420 | 347 | 73 | 347 | 103 | 0 | 103 | 19 | 0 | 347 |
| frontier_temp_1.0_10_run | 1260 | 420 | 348 | 72 | 348 | 97 | 0 | 97 | 20 | 0 | 348 |

## Governed Decision Comparison

See `ten_run_report/AEGIS_10_RUN_HEADLINE.md`, `ten_run_report/AEGIS_10_RUN_GOVERNED_DECISION_TRACE.md`, and grouped bucket summaries.

## Senate Settled Outcome Comparison

Senate escalation means Senate voting path / execution withheld pending scoped signed tally where applicable. Settled Senate decisions are reported separately from the initial Aegis/PDP response.

See `ten_run_report/AEGIS_10_RUN_SENATE_SUMMARY.md`, `ten_run_report/AEGIS_10_RUN_SENATE_BY_SETTLED_DECISION.md`, and `ten_run_report/AEGIS_10_RUN_SENATE_LATENCY_SUMMARY.md`.

## Provenance Comparison

Trusted provenance is counted only when generated on the Aegis/server side from verified policy/source controls. Client/PEP-supplied citations are not accepted as production-valid policy evidence.

See `ten_run_report/AEGIS_10_RUN_PROVENANCE_SUMMARY.md` and `ten_run_report/AEGIS_10_RUN_PROVENANCE_BOUNDARY_AUDIT.md`.

## Risk Outcome Comparison

Aegis-governed risky side-effect completions are zero in this 10x pack. Prompt-policy leakage rows are listed separately with Aegis counterfactual decisions.

See `ten_run_report/AEGIS_10_RUN_RISK_OUTCOME_SUMMARY.md`, `ten_run_report/PROMPT_POLICY_LEAKAGE_WITH_AEGIS_COUNTERFACTUAL.md`, and `ten_run_report/PROMPT_POLICY_LEAKAGE_EVENT_CHAIN.md`.

## Tool, Control, Workflow, And Task Comparison

See `ten_run_report/AEGIS_10_RUN_BY_TOOL_AND_BUCKET.md`, `ten_run_report/AEGIS_10_RUN_BY_CONTROL_AND_BUCKET.md`, `ten_run_report/AEGIS_10_RUN_BY_WORKFLOW_AND_BUCKET.md`, and `ten_run_report/AEGIS_10_RUN_BY_TASK.md`.

## Rerun And Readiness Verdict

This pack was generated from existing artifacts only. It did not rerun models, call Aegis/backend services, mutate policies, mutate prompts, or perform side effects.

See `ten_run_report/AEGIS_10_RUN_PAPER_READINESS.md` and `ten_run_report/AEGIS_10_RUN_RERUN_READINESS_SUMMARY.md`.

## Interpretation Notes

- Raw Aegis decisions are preserved separately from normalized buckets.
- Senate escalation means Senate voting path / execution withheld pending scoped signed tally where applicable.
- A settled Senate `allow` does not mean the original mock tool was applied unless `mock_tool_applied=true`.
- Evidence completeness is distinct from trusted Aegis-resolved provenance validity.
- Client/PEP-supplied citations are not accepted as production-valid policy evidence.
- Existing model outputs were not rerun by this report builder.
