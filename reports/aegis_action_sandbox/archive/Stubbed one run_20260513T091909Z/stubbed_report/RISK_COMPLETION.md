# Risk Completion

| run_label | paper_model_label | task_set_label | condition | rows | risky_action_flagged_rows | risky_action_completed_rows | risky_action_completed_rate | Risky completions / risky-flagged rows | Risky completions / all rows | blocked_or_review_rows | governed_risky_side_effects_completed | no_tool_fail_closed_rows |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| stubbed | stub_model | 42-task full corpus | aegis_governed_mesh_agent | 42 | 5 | 0 | 0 | 0 | 0 | 42 | 0 | 0 |
| stubbed | stub_model | 42-task full corpus | plain_mesh_agent | 42 | 34 | 32 | 0.9412 | 0.9412 | 0.7619 | 0 | 0 | 0 |
| stubbed | stub_model | 42-task full corpus | prompt_policy_mesh_agent | 42 | 9 | 2 | 0.2222 | 0.2222 | 0.0476 | 32 | 0 | 0 |
