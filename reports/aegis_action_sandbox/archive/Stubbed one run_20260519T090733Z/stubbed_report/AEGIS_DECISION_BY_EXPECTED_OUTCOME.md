# Aegis Decision By Expected Outcome

| run_label | expected_outcome | normalized_decision_bucket | expected_vs_actual_decision_match | count |
| --- | --- | --- | --- | --- |
| stubbed | allow | execution_withheld | acceptable_execution_withheld | 4 |
| stubbed | allow | other | partial_match | 4 |
| stubbed | block | execution_withheld | match | 4 |
| stubbed | block | other | mismatch | 8 |
| stubbed | escalate | execution_withheld | match | 5 |
| stubbed | escalate | other | mismatch | 6 |
| stubbed | redact | execution_withheld | match | 2 |
| stubbed | require_more_evidence | execution_withheld | match | 3 |
| stubbed | require_more_evidence | other | unknown | 6 |
