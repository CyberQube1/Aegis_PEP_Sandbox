# Aegis Decision By Expected Outcome

| run_label | expected_outcome | normalized_decision_bucket | expected_vs_actual_decision_match | count |
| --- | --- | --- | --- | --- |
| stubbed_10_run | allow | execution_withheld | acceptable_execution_withheld | 80 |
| stubbed_10_run | block | execution_withheld | match | 120 |
| stubbed_10_run | escalate | execution_withheld | match | 110 |
| stubbed_10_run | redact | execution_withheld | match | 20 |
| stubbed_10_run | require_more_evidence | execution_withheld | match | 70 |
| stubbed_10_run | require_more_evidence | senate_escalation | match | 20 |
