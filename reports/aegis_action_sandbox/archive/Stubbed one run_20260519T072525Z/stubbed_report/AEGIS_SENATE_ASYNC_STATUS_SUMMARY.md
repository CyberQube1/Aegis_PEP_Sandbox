# Aegis Senate Async Status Summary

## Interpretation Notes

- Initial Aegis PDP responses are preserved as execution-withheld / Senate queued decisions in the governed decision trace.
- Settled Senate status is joined from the async Senate snapshot when `senate_escalation_id` is present.
- A Senate-settled `allow` authorizes the governed request path but does not mean the original mock tool was applied in the initial fail-closed response.
- A Senate-settled `deny` confirms the no-side-effect outcome for the original request path.
- `senate_effective_finality_status=final` means a signed tally outcome was observed in the snapshot.

| run_label | senate_rows | snapshot_rows | settled_allowed_rows | settled_denied_rows | settled_failed_closed_rows | settled_unknown_rows | tally_present_rows | quorum_met_rows | effective_final_rows | mock_tool_applied_rows | governed_risky_side_effect_completions | latency_min_ms | latency_p50_ms | latency_p95_ms | latency_max_ms |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| stubbed | 18 | 18 | 0 | 0 | 18 | 0 | 0 | 0 | 18 | 0 | 0 | 12.557 | 13.979 | 49.7035 | 52.551 |
