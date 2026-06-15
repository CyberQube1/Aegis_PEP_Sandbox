# Latency Summary

| run_label | paper_model_label | task_set_label | condition | rows | model_avg_ms | model_median_ms | model_p95_ms | model_max_ms | total_avg_ms | total_median_ms | total_p95_ms | total_max_ms | aegis_avg_ms | aegis_median_ms | Aegis p95 ms | aegis_max_ms |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| stubbed | stub_model | 42-task full corpus | aegis_governed_mesh_agent | 42 | 0.004 | 0.003 | 0.006 | 0.007 | 6573.542 | 6871.06 | 18973.394 | 19641.609 | 6573.279 | 6870.793 | 18973.127 | 19641.381 |
| stubbed | stub_model | 42-task full corpus | plain_mesh_agent | 42 | 0.002 | 0.002 | 0.003 | 0.004 | 0.125 | 0.12 | 0.162 | 0.25 | N/A | N/A | N/A | N/A |
| stubbed | stub_model | 42-task full corpus | prompt_policy_mesh_agent | 42 | 0.002 | 0.002 | 0.002 | 0.002 | 0.141 | 0.134 | 0.177 | 0.206 | N/A | N/A | N/A | N/A |
