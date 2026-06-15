# Latency Summary

| run_label | paper_model_label | task_set_label | condition | rows | model_avg_ms | model_median_ms | model_p95_ms | model_max_ms | total_avg_ms | total_median_ms | total_p95_ms | total_max_ms | aegis_avg_ms | aegis_median_ms | Aegis p95 ms | aegis_max_ms |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| stubbed | stub_model | 42-task full corpus | aegis_governed_mesh_agent | 42 | 0.003 | 0.003 | 0.005 | 0.006 | 44.486 | 42.037 | 68.637 | 78.409 | 44.187 | 41.781 | 68.348 | 78.132 |
| stubbed | stub_model | 42-task full corpus | plain_mesh_agent | 42 | 0.002 | 0.002 | 0.003 | 0.005 | 0.132 | 0.126 | 0.178 | 0.236 | N/A | N/A | N/A | N/A |
| stubbed | stub_model | 42-task full corpus | prompt_policy_mesh_agent | 42 | 0.002 | 0.002 | 0.003 | 0.004 | 0.149 | 0.145 | 0.202 | 0.218 | N/A | N/A | N/A | N/A |
