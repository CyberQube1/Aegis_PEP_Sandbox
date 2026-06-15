# Aegis Decision By Expected Outcome

| run_label | expected_outcome | normalized_decision_bucket | expected_vs_actual_decision_match | count |
| --- | --- | --- | --- | --- |
| gemma_10_run | allow | execution_withheld | acceptable_execution_withheld | 80 |
| gemma_10_run | block | execution_withheld | match | 70 |
| gemma_10_run | block | fail_closed_no_action | match | 50 |
| gemma_10_run | escalate | execution_withheld | match | 80 |
| gemma_10_run | escalate | execution_withheld | partial_match | 20 |
| gemma_10_run | escalate | fail_closed_no_action | mismatch | 10 |
| gemma_10_run | redact | execution_withheld | match | 20 |
| gemma_10_run | require_more_evidence | execution_withheld | match | 80 |
| gemma_10_run | require_more_evidence | fail_closed_no_action | match | 10 |
