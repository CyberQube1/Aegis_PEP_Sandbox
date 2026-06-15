# Latency Summary

| run_label | paper_model_label | task_set_label | condition | rows | model_avg_ms | model_median_ms | model_p95_ms | model_max_ms | total_avg_ms | total_median_ms | total_p95_ms | total_max_ms | aegis_avg_ms | aegis_median_ms | Aegis p95 ms | aegis_max_ms |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| stubbed | stub_model | 42-task full corpus | aegis_governed_mesh_agent | 42 | 0.003 | 0.003 | 0.004 | 0.02 | 66.346 | 65.508 | 103.606 | 118.257 | 69.392 | 65.571 | 104.877 | 117.894 |
| stubbed | stub_model | 42-task full corpus | plain_mesh_agent | 42 | 0.003 | 0.002 | 0.004 | 0.004 | 0.134 | 0.128 | 0.173 | 0.244 | N/A | N/A | N/A | N/A |
| stubbed | stub_model | 42-task full corpus | prompt_policy_mesh_agent | 42 | 0.002 | 0.002 | 0.003 | 0.003 | 0.151 | 0.147 | 0.184 | 0.193 | N/A | N/A | N/A | N/A |
