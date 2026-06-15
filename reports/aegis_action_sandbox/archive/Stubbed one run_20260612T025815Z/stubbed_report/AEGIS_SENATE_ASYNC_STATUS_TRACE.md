# Aegis Senate Async Status Trace

## Interpretation Notes

- Initial Aegis PDP responses are preserved as execution-withheld / Senate queued decisions in the governed decision trace.
- Settled Senate status is joined from the async Senate snapshot when `senate_escalation_id` is present.
- A Senate-settled `allow` authorizes the governed request path but does not mean the original mock tool was applied in the initial fail-closed response.
- A Senate-settled `deny` confirms the no-side-effect outcome for the original request path.
- `senate_effective_finality_status=final` means a signed tally outcome was observed in the snapshot.

_No rows._
