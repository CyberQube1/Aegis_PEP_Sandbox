# Latency Summary

| run_label | paper_model_label | task_set_label | condition | rows | model_avg_ms | model_median_ms | model_p95_ms | model_max_ms | total_avg_ms | total_median_ms | total_p95_ms | total_max_ms | aegis_avg_ms | aegis_median_ms | Aegis p95 ms | aegis_max_ms |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| stubbed | stub_model | 42-task full corpus | aegis_governed_mesh_agent | 42 | 0.004 | 0.004 | 0.004 | 0.005 | 26.588 | 24.078 | 26.181 | 125.179 | 26.317 | 23.805 | 25.934 | 124.932 |
| stubbed | stub_model | 42-task full corpus | plain_mesh_agent | 42 | 0.002 | 0.002 | 0.003 | 0.004 | 0.109 | 0.106 | 0.132 | 0.24 | N/A | N/A | N/A | N/A |
| stubbed | stub_model | 42-task full corpus | prompt_policy_mesh_agent | 42 | 0.002 | 0.002 | 0.002 | 0.003 | 0.141 | 0.137 | 0.179 | 0.207 | N/A | N/A | N/A | N/A |
