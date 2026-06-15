# Prompt-Policy Leakage Event Chain

This report reconstructs each prompt-policy leakage event from the run artifacts and joins it to the governed Aegis counterfactual for the same run/task, including available cryptographic/audit anchors.

Interpretation notes:
- Prompt-policy and plain lanes do not call Aegis, so they do not normally have Aegis ILK or decision receipts.
- Aegis-governed rows expose decision trace anchors such as decision ID, trace ID, deterministic decision hash, policy graph hashes, source citation digests, and timing marks when present in the artifact.
- `ilk_receipt_refs_available=false` means this artifact did not preserve an ILK append receipt reference for that row; it does not mean the Aegis decision was unsafe.
- `bridge_audit_enqueued_ms` is a timing mark that the bridge audit enqueue path ran; it is not itself an ILK receipt hash.
- No model, Aegis/backend, Senate, or ILK service calls are made while generating this report.

No prompt-policy leakage event-chain rows found in selected runs.
