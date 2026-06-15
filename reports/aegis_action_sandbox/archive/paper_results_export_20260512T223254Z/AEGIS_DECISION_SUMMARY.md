# Aegis Decision Summary

| run_label | paper_model_label | condition | rows | aegis_attempted_rows | aegis_avg_ms | aegis_median_ms | aegis_p95_ms | aegis_max_ms | mock_tool_applied_rows | no_tool_fail_closed_rows |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| gemma | open_model_a | aegis_governed_mesh_agent | 42 | 35 | 72.575 | 64.326 | 94.605 | 273.506 | 0 | 7 |
| gemma | open_model_a | aegis_governed_mesh_agent | 35 |  |  |  |  |  |  | decision=block |
| gemma | open_model_a | aegis_governed_mesh_agent | 7 |  |  |  |  |  |  | decision=fail_closed_no_action |
