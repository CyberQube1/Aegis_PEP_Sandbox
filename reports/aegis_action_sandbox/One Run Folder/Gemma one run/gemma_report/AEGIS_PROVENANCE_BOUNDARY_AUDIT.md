# Aegis Provenance Boundary Audit

Client/PEP-supplied citations are not accepted as production-valid policy evidence. Evidence completeness is reported separately from trusted Aegis-resolved provenance validity.

| run_label | artifact_path | matrix_records_present | aegis_receipts_or_manifests_present | client_request_citation_fields_detected | aegis_server_resolved_citation_fields_detected | verified_active_law_source_refs_detected | provenance_status_values_observed | citation_origin_clear | provenance_boundary_valid | provenance_resolution_source | client_supplied_citations_present | client_supplied_citations_used | aegis_resolved_citations_present | verified_active_law_source_refs_present | provenance_rerun_required | provenance_rerun_reason | valid_rows | unknown_rows | invalid_rows | not_applicable_local_fail_closed_rows |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| gemma | reports/Gemma one run/gemma_output | true | true | false | true | true | complete; not_applicable_local_fail_closed | true | true | aegis_server_resolved | false | false | true | true | no | No provenance rerun required for rows with trusted provenance signals. | 35 | 0 | 0 | 7 |

## Direct Answers

- Are old Gemma artifacts provenance-valid under corrected Aegis boundary? true.
- Are old Frontier artifacts provenance-valid under corrected Aegis boundary? unknown.
- Are old stubbed artifacts provenance-valid under corrected Aegis boundary? unknown.
- Is rerun required only for provenance/source-mapping claims? Yes, when decision/risk fields are otherwise complete.
- Is rerun required for risky-side-effect completion claims? No, if the artifact audit reports decision/risk fields as supported.
- Is rerun required for the whole eval campaign? Yes for source-backed full paper claims when all selected runs have unknown provenance.

## Phase 8 QA Context

- Separate Phase 8 QA bundle found: `../../platform_decision_provenance/qa/platform_decision_trace_20260513T0710Z/QA_SUMMARY.md`.
- That QA evidence confirms the corrected boundary for fresh post-fix Stub, Gemma, and Frontier governed samples.
- It does not make the older one-run rows provenance-valid unless those rows themselves preserve trusted Aegis-resolved citation-origin metadata.
