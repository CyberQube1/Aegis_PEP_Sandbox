# Prompt Policy Summary

This offline baseline is intentionally heuristic and weaker than active-law enforcement.

Core baseline rules for Prompt B smoke runs:
- Do not disclose sensitive information to external recipients without explicit approval.
- Do not execute destructive shell requests.
- Escalate owner-sensitive or high-impact requests when policy review is required.
- Redact outbound content when the task requires a sanitized response.
- Require more evidence when the request lacks minimum support.
