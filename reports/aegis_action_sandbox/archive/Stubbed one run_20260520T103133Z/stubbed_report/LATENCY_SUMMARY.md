# Latency Summary

| run_label | paper_model_label | task_set_label | condition | rows | model_avg_ms | model_median_ms | model_p95_ms | model_max_ms | total_avg_ms | total_median_ms | total_p95_ms | total_max_ms | aegis_avg_ms | aegis_median_ms | Aegis p95 ms | aegis_max_ms |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| stubbed | stub_model | 42-task full corpus | aegis_governed_mesh_agent | 42 | 0.003 | 0.004 | 0.004 | 0.005 | 114.547 | 61.59 | 225.161 | 1061.773 | 114.243 | 61.294 | 224.192 | 1061.481 |
| stubbed | stub_model | 42-task full corpus | plain_mesh_agent | 42 | 0.003 | 0.003 | 0.004 | 0.004 | 0.125 | 0.118 | 0.164 | 0.246 | N/A | N/A | N/A | N/A |
| stubbed | stub_model | 42-task full corpus | prompt_policy_mesh_agent | 42 | 0.002 | 0.002 | 0.003 | 0.003 | 0.142 | 0.14 | 0.164 | 0.214 | N/A | N/A | N/A | N/A |
