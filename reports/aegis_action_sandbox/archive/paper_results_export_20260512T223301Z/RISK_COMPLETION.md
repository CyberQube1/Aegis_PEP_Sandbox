# Risk Completion

| run_label | paper_model_label | condition | rows | risky_action_flagged_rows | risky_action_completed_rows | risky_action_completed_rate | blocked_or_review_rows | governed_risky_side_effects_completed | no_tool_fail_closed_rows |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| frontier | frontier_model_a | aegis_governed_mesh_agent | 36 | 0 | 0 | 0 | 36 | 0 | 9 |
| frontier | frontier_model_a | plain_mesh_agent | 36 | 18 | 18 | 1 | 15 | 0 | 9 |
| frontier | frontier_model_a | prompt_policy_mesh_agent | 36 | 3 | 1 | 0.3333 | 32 | 0 | 10 |
| gemma | open_model_a | aegis_governed_mesh_agent | 42 | 7 | 0 | 0 | 42 | 0 | 7 |
| gemma | open_model_a | plain_mesh_agent | 42 | 26 | 19 | 0.7308 | 17 | 0 | 7 |
| gemma | open_model_a | prompt_policy_mesh_agent | 42 | 6 | 0 | 0 | 37 | 0 | 9 |
| stub | stub_model | aegis_governed_mesh_agent | 36 | 4 | 0 | 0 | 36 | 0 | 0 |
| stub | stub_model | plain_mesh_agent | 36 | 29 | 27 | 0.931 | 0 | 0 | 0 |
| stub | stub_model | prompt_policy_mesh_agent | 36 | 8 | 2 | 0.25 | 27 | 0 | 0 |
