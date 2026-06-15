# Aegis Artifact Audit

## Direct Answers

- Can we regenerate full governed-decision reports from existing artifacts? yes.
- Do we need to rerun Gemma? unknown.
- Do we need to rerun Frontier temp 0? unknown.
- Do we need to rerun Frontier temp 0.7? unknown.
- Do we need to rerun Frontier temp 1.0? unknown.
- Do we need to rerun stubbed? yes.
- Do we need to rerun everything? yes.
- Is rerun needed for risk-outcome claims? no.
- Is rerun needed for provenance/source-mapping claims? yes.
- Is rerun needed for full paper claims? yes.

## Run Field Audit

| run_label | input_run_directory | matrix_records_jsonl_present | row_count | governed_row_count | aegis_attempted_rows | report_regeneration_possible_without_rerunning_inference | risky_side_effect_outcome_claims_supported | provenance_source_mapping_claims_supported | full_paper_claims_supported | fields_missing |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| stubbed | outputs_island/stubbed_one_run_20260525T072712Z | true | 126 | 42 | 42 | true | true | false | false | N/A |

## Rerun Decision

- Recommendation: `rerun_all_runs`
- Reason: Trusted Aegis-resolved citation origin is not proven in existing artifacts.

## Phase 8 QA Context

- Separate Phase 8 QA bundle found: `../../platform_decision_provenance/qa/platform_decision_trace_20260513T0710Z/QA_SUMMARY.md`.
- That QA evidence confirms the corrected boundary for fresh post-fix Stub, Gemma, and Frontier governed samples.
- It does not make the older one-run rows provenance-valid unless those rows themselves preserve trusted Aegis-resolved citation-origin metadata.
