# Aegis Decision By Expected Outcome

| run_label | expected_outcome | normalized_decision_bucket | expected_vs_actual_decision_match | count |
| --- | --- | --- | --- | --- |
| stubbed | allow | execution_withheld | acceptable_execution_withheld | 8 |
| stubbed | block | allow_or_approve | mismatch | 2 |
| stubbed | block | execution_withheld | match | 10 |
| stubbed | escalate | execution_withheld | match | 11 |
| stubbed | redact | execution_withheld | match | 2 |
| stubbed | require_more_evidence | execution_withheld | match | 7 |
| stubbed | require_more_evidence | fail_closed_no_action | match | 2 |
