# Latency Summary

| run_label | paper_model_label | task_set_label | condition | rows | model_avg_ms | model_median_ms | model_p95_ms | model_max_ms | total_avg_ms | total_median_ms | total_p95_ms | total_max_ms | aegis_avg_ms | aegis_median_ms | Aegis p95 ms | aegis_max_ms |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| stubbed_10_run | stub_model | 42-task full corpus | aegis_governed_mesh_agent | 420 | 0.004 | 0.004 | 0.006 | 0.02 | 28.804 | 28.047 | 33.861 | 71.284 | 28.504 | 27.754 | 33.58 | 71.003 |
| stubbed_10_run | stub_model | 42-task full corpus | plain_mesh_agent | 420 | 0.002 | 0.002 | 0.004 | 0.019 | 0.119 | 0.111 | 0.178 | 0.278 | N/A | N/A | N/A | N/A |
| stubbed_10_run | stub_model | 42-task full corpus | prompt_policy_mesh_agent | 420 | 0.002 | 0.002 | 0.003 | 0.014 | 0.144 | 0.14 | 0.183 | 0.365 | N/A | N/A | N/A | N/A |
