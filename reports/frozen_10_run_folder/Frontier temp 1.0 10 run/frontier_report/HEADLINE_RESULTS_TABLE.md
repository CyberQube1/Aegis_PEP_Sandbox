# Headline Results Table

| run_label | paper_model_label | task_set_label | condition | rows | risky_action_completed_rows | Risky completions / risky-flagged rows | Risky completions / all rows | mock_tool_applied_rows | Evidence completeness rate | aegis_attempted_rows | Aegis p95 ms |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| frontier_temp_1.0_10_run | frontier_model_a | 42-task full corpus | aegis_governed_mesh_agent | 420 | 0 | 0 | 0 | 0 | 1 | 348 | 64.528 |
| frontier_temp_1.0_10_run | frontier_model_a | 42-task full corpus | plain_mesh_agent | 420 | 266 | 0.9925 | 0.6333 | 296 | 1 | 0 | N/A |
| frontier_temp_1.0_10_run | frontier_model_a | 42-task full corpus | prompt_policy_mesh_agent | 420 | 20 | 0.4651 | 0.0476 | 160 | 1 | 0 | N/A |
