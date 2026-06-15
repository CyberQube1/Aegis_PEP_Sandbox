# Latency Summary

| run_label | paper_model_label | task_set_label | condition | rows | model_avg_ms | model_median_ms | model_p95_ms | model_max_ms | total_avg_ms | total_median_ms | total_p95_ms | total_max_ms | aegis_avg_ms | aegis_median_ms | Aegis p95 ms | aegis_max_ms |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| stubbed | stub_model | 42-task full corpus | aegis_governed_mesh_agent | 42 | 0.003 | 0.003 | 0.004 | 0.014 | 24.578 | 23.738 | 27.602 | 34.053 | 24.328 | 23.494 | 27.347 | 33.861 |
| stubbed | stub_model | 42-task full corpus | plain_mesh_agent | 42 | 0.002 | 0.002 | 0.003 | 0.004 | 0.11 | 0.106 | 0.136 | 0.229 | N/A | N/A | N/A | N/A |
| stubbed | stub_model | 42-task full corpus | prompt_policy_mesh_agent | 42 | 0.002 | 0.002 | 0.002 | 0.003 | 0.13 | 0.129 | 0.147 | 0.184 | N/A | N/A | N/A | N/A |
