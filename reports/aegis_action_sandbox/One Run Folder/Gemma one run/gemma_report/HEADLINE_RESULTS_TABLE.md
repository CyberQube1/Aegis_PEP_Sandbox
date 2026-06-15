# Headline Results Table

| run_label | paper_model_label | task_set_label | condition | rows | risky_action_completed_rows | Risky completions / risky-flagged rows | Risky completions / all rows | mock_tool_applied_rows | Evidence completeness rate | aegis_attempted_rows | Aegis p95 ms |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| gemma | open_model_a | 42-task full corpus | aegis_governed_mesh_agent | 42 | 0 | 0 | 0 | 0 | 1 | 35 | 47.147 |
| gemma | open_model_a | 42-task full corpus | plain_mesh_agent | 42 | 19 | 0.7308 | 0.4524 | 25 | 1 | 0 | N/A |
| gemma | open_model_a | 42-task full corpus | prompt_policy_mesh_agent | 42 | 0 | 0 | 0 | 15 | 1 | 0 | N/A |
