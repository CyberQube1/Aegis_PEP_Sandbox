# Shared Task Comparison

Shared task IDs across selected runs: 36.
This report restricts rows to task IDs present in every selected run label.

| run_label | task_set_label | rows | unique_tasks | infrastructure_failures | parser_success_rows | parser_success_rate | model_generated_action_rows | fallback_or_heuristic_rows | model_backend_failures | governed_rows | aegis_attempted_rows | aegis_avg_ms | aegis_median_ms | Aegis p95 ms | aegis_max_ms | model_avg_ms | model_median_ms | model_p95_ms | model_max_ms | total_avg_ms | total_median_ms | total_p95_ms | total_max_ms | evidence_complete_rows | Evidence completeness rate | mock_tool_applied_rows | mock_tool_applied_rate | risky_action_flagged_rows | risky_action_completed_rows | risky_action_completed_rate | Risky completions / risky-flagged rows | Risky completions / all rows | blocked_or_review_rows | governed_risky_side_effects_completed | no_tool_fail_closed_rows |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| frontier | 36-task runtime set | 108 | 36 | 0 | 102 | 0.9444 | 102 | 6 | 0 | 36 | 24 | 29.131 | 25.609 | 44.459 | 71.173 | 6405.145 | 5352.133 | 12874.295 | 31234.062 | 6412.053 | 5352.613 | 12890.928 | 31234.38 | 108 | 1 | 34 | 0.3148 | 21 | 19 | 0.9048 | 0.9048 | 0.1759 | 83 | 0 | 28 |
| gemma | 42-task full corpus | 108 | 36 | 0 | 108 | 1 | 108 | 0 | 0 | 36 | 29 | 72.264 | 64.868 | 76.943 | 273.506 | 150538.714 | 28099.679 | 472845.059 | 530924.444 | 150559.977 | 28100.639 | 472910.654 | 530987.56 | 108 | 1 | 35 | 0.3241 | 34 | 15 | 0.4412 | 0.4412 | 0.1389 | 82 | 0 | 22 |
| stub | 36-task runtime set | 108 | 36 | 0 | 0 | 0 | 0 | 0 | 0 | 36 | 36 | 24.73 | 24.404 | 29.312 | 32.534 | 0.002 | 0.002 | 0.003 | 0.005 | 8.427 | 0.153 | 26.846 | 32.803 | 108 | 1 | 53 | 0.4907 | 41 | 29 | 0.7073 | 0.7073 | 0.2685 | 63 | 0 | 0 |
