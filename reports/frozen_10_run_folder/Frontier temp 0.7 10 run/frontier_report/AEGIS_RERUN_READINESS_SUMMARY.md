# Aegis Rerun Readiness Summary

- Existing artifacts sufficient for governed-decision and risky-side-effect reporting: yes.
- Rerun needed for risk outcomes: no.
- Rerun needed for provenance/source-mapping claims: no.
- Rerun needed for full paper claims: no.
- Gemma rerun needed: unknown.
- Frontier temp 0 rerun needed: no.
- Frontier temp 0.7 rerun needed: unknown.
- Frontier temp 1.0 rerun needed: unknown.
- Stubbed rerun needed: unknown.
- All rerun needed: no.
- Recommendation: `no_rerun_needed`.
- Reason: Existing artifacts support decision, risk, and trusted provenance claims.

## If Rerunning Is Chosen

Run the separate rerun script; report generation alone does not call models or Aegis/backend services.

```bash
./scripts/run_all_one_run_campaign.sh
```

Expected output folders are the five one-run report folders and `reports/all one run comparison/comparison_report/`.
