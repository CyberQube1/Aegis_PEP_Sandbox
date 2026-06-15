# Aegis Governed Decision Headline

## Interpretation Notes

- Raw Aegis decisions are preserved separately from normalized buckets.
- Senate escalation means Senate voting path / execution withheld pending scoped signed tally where reason codes indicate that state.
- Execution-withheld rows did not apply mock tools unless `mock_tool_applied` is true.
- Local fail-closed/no-action rows did not attempt Aegis because the model proposed no side-effectful tool/action.
- Evidence completeness is distinct from trusted Aegis-resolved provenance validity.
- Client/PEP-supplied citations are not accepted as production-valid policy evidence.
- Existing model outputs were not rerun unless the audit/rerun script explicitly says they were.

| run_label | paper_model_label | governed_rows | aegis_attempted_rows | allow_or_approve_rows | block_rows | senate_escalation_rows | execution_withheld_rows | fail_closed_no_action_rows | parser_or_backend_failure_rows | other_rows | mock_tool_applied_rows | governed_risky_side_effect_completions | evidence_complete_rows | evidence_completeness_rate | provenance_boundary_valid_rows | provenance_boundary_unknown_rows | provenance_boundary_invalid_rows | rerun_needed_for_risk_outcome_claims | rerun_needed_for_provenance_claims | rerun_needed_for_full_paper_claims | rerun_recommended | rerun_reason_short |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| stubbed | stub_model | 42 | 42 | 0 | 2 | 2 | 38 | 0 | 0 | 0 | 0 | 0 | 42 | 1.0 | 0 | 42 | 0 | false | true | true | rerun_all_runs | Existing artifacts support decision/risk reporting, but trusted Aegis-resolved provenance is not proven. |
