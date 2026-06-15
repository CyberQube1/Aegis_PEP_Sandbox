# Aegis Rerun Readiness Summary

- Existing artifacts sufficient for governed-decision and risky-side-effect reporting: yes.
- Rerun needed for risk outcomes: no.
- Rerun needed for provenance/source-mapping claims: yes.
- Rerun needed for full paper claims: yes.
- Gemma rerun needed: unknown.
- Frontier temp 0 rerun needed: unknown.
- Frontier temp 0.7 rerun needed: unknown.
- Frontier temp 1.0 rerun needed: unknown.
- Stubbed rerun needed: yes.
- All rerun needed: yes.
- Recommendation: `rerun_all_runs`.
- Reason: Trusted Aegis-resolved citation origin is not proven in existing artifacts.

## If Rerunning Is Chosen

Run the separate rerun script; report generation alone does not call models or Aegis/backend services.

```bash
./scripts/run_all_one_run_campaign.sh
```

Expected output folders are the five one-run report folders and `reports/all one run comparison/comparison_report/`.
