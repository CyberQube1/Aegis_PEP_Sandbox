# Latency Summary

| run_label | paper_model_label | task_set_label | condition | rows | model_avg_ms | model_median_ms | model_p95_ms | model_max_ms | total_avg_ms | total_median_ms | total_p95_ms | total_max_ms | aegis_avg_ms | aegis_median_ms | Aegis p95 ms | aegis_max_ms |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| stubbed | stub_model | 42-task full corpus | aegis_governed_mesh_agent | 42 | 0.004 | 0.004 | 0.005 | 0.006 | 28.105 | 25.552 | 31.704 | 108.818 | 27.809 | 25.24 | 31.387 | 108.576 |
| stubbed | stub_model | 42-task full corpus | plain_mesh_agent | 42 | 0.002 | 0.002 | 0.003 | 0.004 | 0.112 | 0.11 | 0.125 | 0.243 | N/A | N/A | N/A | N/A |
| stubbed | stub_model | 42-task full corpus | prompt_policy_mesh_agent | 42 | 0.002 | 0.002 | 0.003 | 0.003 | 0.146 | 0.143 | 0.176 | 0.281 | N/A | N/A | N/A | N/A |
