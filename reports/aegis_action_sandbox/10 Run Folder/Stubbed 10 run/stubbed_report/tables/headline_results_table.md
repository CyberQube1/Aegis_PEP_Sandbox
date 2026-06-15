| run_label | paper_model_label | task_set_label | condition | rows | risky_action_completed_rows | Risky completions / risky-flagged rows | Risky completions / all rows | mock_tool_applied_rows | Evidence completeness rate | aegis_attempted_rows | Aegis p95 ms |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| stubbed_10_run | stub_model | 42-task full corpus | aegis_governed_mesh_agent | 420 | 0 | 0 | 0 | 0 | 1 | 420 | 33.58 |
| stubbed_10_run | stub_model | 42-task full corpus | plain_mesh_agent | 420 | 320 | 0.9412 | 0.7619 | 400 | 1 | 0 | N/A |
| stubbed_10_run | stub_model | 42-task full corpus | prompt_policy_mesh_agent | 420 | 20 | 0.2222 | 0.0476 | 220 | 1 | 0 | N/A |
