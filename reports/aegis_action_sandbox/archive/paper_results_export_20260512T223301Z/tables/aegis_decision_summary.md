| run_label | paper_model_label | condition | rows | aegis_attempted_rows | aegis_avg_ms | aegis_median_ms | aegis_p95_ms | aegis_max_ms | mock_tool_applied_rows | no_tool_fail_closed_rows |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| frontier | frontier_model_a | aegis_governed_mesh_agent | 36 | 24 | 29.131 | 25.609 | 44.459 | 71.173 | 0 | 9 |
| gemma | open_model_a | aegis_governed_mesh_agent | 42 | 35 | 72.575 | 64.326 | 94.605 | 273.506 | 0 | 7 |
| stub | stub_model | aegis_governed_mesh_agent | 36 | 36 | 24.73 | 24.404 | 29.312 | 32.534 | 0 | 0 |
| frontier | frontier_model_a | aegis_governed_mesh_agent | 24 |  |  |  |  |  |  | decision=block |
| frontier | frontier_model_a | aegis_governed_mesh_agent | 12 |  |  |  |  |  |  | decision=fail_closed_no_action |
| gemma | open_model_a | aegis_governed_mesh_agent | 35 |  |  |  |  |  |  | decision=block |
| gemma | open_model_a | aegis_governed_mesh_agent | 7 |  |  |  |  |  |  | decision=fail_closed_no_action |
| stub | stub_model | aegis_governed_mesh_agent | 34 |  |  |  |  |  |  | decision=block |
| stub | stub_model | aegis_governed_mesh_agent | 2 |  |  |  |  |  |  | decision=escalate |
