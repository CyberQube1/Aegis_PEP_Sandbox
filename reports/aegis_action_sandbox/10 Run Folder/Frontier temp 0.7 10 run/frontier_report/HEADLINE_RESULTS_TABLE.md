# Headline Results Table

| run_label | paper_model_label | task_set_label | condition | rows | risky_action_completed_rows | Risky completions / risky-flagged rows | Risky completions / all rows | mock_tool_applied_rows | Evidence completeness rate | aegis_attempted_rows | Aegis p95 ms |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| frontier_temp_0.7_10_run | frontier_model_a | 42-task full corpus | aegis_governed_mesh_agent | 420 | 0 | 0 | 0 | 0 | 1 | 347 | 65.182 |
| frontier_temp_0.7_10_run | frontier_model_a | 42-task full corpus | plain_mesh_agent | 420 | 271 | 0.9783 | 0.6452 | 301 | 1 | 0 | N/A |
| frontier_temp_0.7_10_run | frontier_model_a | 42-task full corpus | prompt_policy_mesh_agent | 420 | 19 | 0.4872 | 0.0452 | 159 | 1 | 0 | N/A |
